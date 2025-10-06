from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import os
import numpy as np
import glob
from typing import List, Dict, Any, Optional, Union, Tuple
from langchain.schema import Document
from bs4 import BeautifulSoup
import feedparser
from langchain import hub
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
import sentence_transformers
from pathlib import Path
from langchain_core.embeddings import Embeddings
from typing import List
import pickle
import requests
import json
import logging
import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log/news_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('NewsCrawler')

class NewsCrawler:
    def __init__(self, output_dir="news"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.date_suffix = (str)(datetime.datetime.today().date()).replace("-", "_")
        self.news_path = os.path.join(self.output_dir, self.date_suffix)
        os.makedirs(self.news_path, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def crawl_news_sites(self):
        """爬取多个新闻网站"""
        logger.info("开始执行新闻爬取任务")
        
        news_data = []
        
        try:
            # 通过RSS获取新闻
            news_data.extend(self.crawl_rss_feeds())
            
        except Exception as e:
            logger.error(f"爬取过程中出错: {e}")
        
        # 保存新闻数据
        self.save_news(news_data)
        logger.info(f"爬取完成，共获取 {len(news_data)} 条新闻")
        
        return news_data
    
    def crawl_rss_feeds(self):
        """通过RSS订阅获取新闻"""
        rss_feeds = {
            "新浪新闻": "http://rss.sina.com.cn/news/china/focus15.xml",
            "搜狐新闻": "http://rss.news.sohu.com/rss/focus.xml", 
        }
        
        news_list = []
        for _, feed_url in rss_feeds.items():
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    news_list.append({
                        'title': entry.title,
                        'link': entry.link,
                        'source': 'RSS-' + feed_url.split('/')[-2],
                        'crawled_at': datetime.datetime.now().isoformat(),
                        'summary': entry.get('summary', '')[:200]
                    })
            except Exception as e:
                logger.error(f"解析RSS源 {feed_url} 失败: {e}")
        
        os.environ["NewsCount"] = str(len(news_list))

        logger.info(f"从RSS源获取 {len(news_list)} 条新闻")
        return news_list
    
    def save_news(self, news_data):
        """保存新闻数据到文件"""
        if not news_data:
            return
        
        # 按日期创建文件
        os.makedirs(self.news_path, exist_ok=True)
        filename = self.output_dir/ self.date_suffix / f"news_{self.date_suffix}.json"
        
        # 保存为JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        # 同时保存为文本文件，便于后续处理
        txt_filename = self.output_dir / self.date_suffix / f"news_{self.date_suffix}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            for news in news_data:
                f.write(f"标题: {news['title']}\n")
                f.write(f"来源: {news['source']}\n")
                f.write(f"链接: {news['link']}\n")
                f.write(f"时间: {news['crawled_at']}\n")
                if 'summary' in news:
                    f.write(f"摘要: {news['summary']}\n")
                f.write("-" * 50 + "\n\n")
        
        logger.info(f"新闻数据已保存到: {filename} 和 {txt_filename}")

class SentenceTransformerEmbeddings(Embeddings):
    """自定义的SentenceTransformer嵌入包装器"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = sentence_transformers.SentenceTransformer(model_name)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """为文档生成嵌入"""
        embeddings = self.model.encode(
            texts, 
            convert_to_numpy=True, 
            normalize_embeddings=True
        )
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """为查询生成嵌入"""
        embedding = self.model.encode(
            [text], 
            convert_to_numpy=True, 
            normalize_embeddings=True
        )
        return embedding[0].tolist()

class DailyFAISSHelper:
    def __init__(self, dimension: int = 384, retention_days: int = 7):
        """
        按日期分片的FAISS向量数据库助手
        
        Args:
            base_dir: 数据存储基础目录
            dimension: 向量维度
            retention_days: 数据保留天数
        """

        current_file = Path(__file__)
        
        self.base_dir = current_file.parent.parent.parent / "news"
        self.save_dir = current_file.parent.parent.parent / "instance" / "faiss"
        self.date_suffix = (str)(datetime.datetime.today().date()).replace("-", "_")
        self.dimension = dimension
        self.retention_days = retention_days
        
        self.embedding_function = SentenceTransformerEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.faiss_dir = (str)(os.path.join(self.save_dir, f"faiss_{self.date_suffix}"))
        self.index_path = os.path.join(self.faiss_dir, "index_" + self.date_suffix + ".faiss")
        self.file_path = os.path.join(self.faiss_dir, "index_" + self.date_suffix + ".pkl")
        self.vector = FAISS(
            embedding_function=self.embedding_function,
            index=faiss.IndexFlatL2(dimension),
            docstore=InMemoryDocstore({}),
            index_to_docstore_id={}
        )

        # 确保基础目录存在
        try:
            if os.path.exists(self.base_dir) is False:
                logger.warning("新闻目录不存在，无法初始化DailyFAISSHelper")

        except Exception as e:
            logger.error("初始化失败")
        
        logger.info(f"初始化DailyFAISSHelper，基础目录: {self.base_dir}, 维度: {dimension}, 保留天数: {retention_days}")
    
    def save_faiss_from_json(self):
        
        try:
            # 确定要处理的JSON文件路径
            json_file_path = self.base_dir / self.date_suffix / f"news_{self.date_suffix}.json"
            
            if not os.path.exists(json_file_path):
                logger.warning(f"新闻JSON文件不存在: {json_file_path}")
                return False
            
            # 加载新闻数据
            with open(json_file_path, 'r', encoding='utf-8') as f:
                news_data = json.load(f)
            
            documents = []
            for i, news_item in enumerate(news_data):
                # 构建文档内容
                content_parts = []
                if 'title' in news_item:
                    content_parts.append(f"标题: {news_item['title']}")
                if 'summary' in news_item and news_item['summary']:
                    content_parts.append(f"摘要: {news_item['summary']}")
                
                content = "\n".join(content_parts)
                
                # 构建元数据
                metadata = {
                    'source': news_item.get('source', 'unknown'),
                    'link': news_item.get('link', ''),
                    'crawled_at': news_item.get('crawled_at', ''),
                    'news_id': f"{self.date_suffix}_{i}",
                    'type': 'news'
                }
                
                # 创建Document对象
                document = Document(
                    page_content=content,
                    metadata=metadata
                )
                documents.append(document)
            
            logger.info(f"从 {json_file_path} 加载了 {len(documents)} 条新闻")
            
        
            if not documents:
                logger.warning("没有加载到任何新闻数据")
                return False
            
            # 分割文档
            all_splits = []
            for doc in documents:
                splits = self.text_splitter.split_documents([doc])
                all_splits.extend(splits)
            
            logger.info(f"原始文档数: {len(documents)}, 分割后文档块数: {len(all_splits)}")
            
            # 添加到向量数据库
            if all_splits:
                # 获取当前向量数量
                start_count = self.vector.index.ntotal
                
                # 添加文档到向量数据库
                self.vector.add_documents(all_splits)
                
                # 记录添加的向量数量
                added_count = self.vector.index.ntotal - start_count
                logger.info(f"成功添加 {added_count} 个文档块到向量数据库")
                
                return True
            else:
                logger.warning("没有文档块可以添加到向量数据库")
                
            # 保存索引
            faiss.write_index(self.vector.index, str(self.index_path))
            
            # 保存文档数据
            with open(self.file_path, 'wb') as f:
                pickle.dump({
                    'docstore': self.vector.docstore._dict,
                    'index_to_docstore_id': self.vector.index_to_docstore_id
                }, f)
            
            print(f"保存成功到: {self.save_dir}")
            

        except Exception as e:
            logger.error(f"保存FAISS索引失败: {e}")
            return False

    def print_pkl_contents(self):
        """
        打印PKL文件的内容
        
        Args:
            data: PKL文件中保存的数据
        """
        print("\n" + "="*80)
        print("PKL 文件内容:")
        print("="*80)
        
        with open(self.file_path, "rb") as data:
            data = pickle.load(data)
            # 打印基本信息
            print(f"文档存储数量: {len(data['docstore'])}")
            print(f"索引到文档ID映射数量: {len(data['index_to_docstore_id'])}")
            
            # 打印文档存储内容
            print("\n文档存储 (docstore) 内容:")
            print("-" * 40)
            for i, (doc_id, doc) in enumerate(list(data['docstore'].items())[:5]):  # 只显示前5个
                print(f"文档ID: {doc_id}")
                print(f"  内容: {doc.page_content[:100]}...")  # 只显示前100个字符
                print(f"  元数据: {doc.metadata}")
                print()
            
            if len(data['docstore']) > 5:
                print(f"... 还有 {len(data['docstore']) - 5} 个文档未显示")
            
            # 打印索引映射内容
            print("\n索引到文档ID映射 (index_to_docstore_id) 内容:")
            print("-" * 40)
            print(f"前10个映射: {data['index_to_docstore_id'][:10]}")
            print(f"映射总数: {len(data['index_to_docstore_id'])}")
            
            print("="*80 + "\n")

    
    
    

# class State(TypedDict):
#         question: str
#         context: List[Document]
#         answer: str


#     # Define application steps
# def retrieve(state: State):
#     retrieved_docs = vector_store.similarity_search(state["question"])
#     return {"context": retrieved_docs}


# def generate(state: State):
#     docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    
#     improved_prompt = \
#     f"""基于以下上下文回答问题。如果上下文没有相关信息，请明确说明"根据提供的资料，没有找到相关信息"。

#         上下文：
#         {docs_content}

#         问题：{state["question"]}

#         要求：
#         1. 严格基于上下文信息回答
#         2. 如果上下文没有相关信息，不要编造答案
#         3. 如果信息不完整，请说明哪些方面缺乏信息

#     回答："""
#     # 修复：直接使用返回的响应
#     response = llm.invoke(improved_prompt)
    
#     # 简单的类型检查
#     if isinstance(response, str):
#         return {"answer": response}
#     elif hasattr(response, 'content'):
#         return {"answer": response.content}
#     else:
#         return {"answer": str(response)}

# if __name__ == "__main__":
    
#     embedding_model = SentenceTransformerEmbeddings('sentence-transformers/all-MiniLM-L6-v2')
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     llm = Ollama(
#         model="qwen3:8b", 
#         temperature=0.7,
#         num_predict=2048
#     )

#     current_file = Path(__file__)
#     news_dir = current_file.parent.parent.parent / "news"
#     index_dir = current_file.parent.parent.parent / "instance"
#     # print(f"news目录路径: {news_dir}")

#     vector_store = load_faiss_simple(embedding_model, index_dir)
#     # 检查目录是否存在
#     # if not os.path.isdir(news_dir):
#     #     print(f"Error: Directory not found at {news_dir}")
#     # else:
#     #     # 遍历news目录下的所有文件
#     #     for filename in os.listdir(news_dir):
#     #         file_path = os.path.join(news_dir, filename)
#     #         # 确保是文件而不是子目录
#     #         if os.path.isfile(file_path):
#     #             try:
#     #                 with open(file_path, "r", encoding='utf-8') as f:
#     #                     content = f.read()
                        
#     #                     all_splits = text_splitter.split_text(content)
#     #                     vector_store.add_texts(all_splits)

#     #             except Exception as e:
#     #                 print(f"Error reading file {filename}: {e}")

    
#     # save_faiss_simple(vector_store, index_dir)

#     # 查看向量存储的基本信息
#     print(f"向量数量: {vector_store.index.ntotal}")
#     print(f"向量维度: {vector_store.index.d}")

#     # 查看索引到文档的映射
#     print(f"索引映射数量: {len(vector_store.index_to_docstore_id)}")

#     prompt = hub.pull("rlm/rag-prompt")

#     # Compile application and test
#     graph_builder = StateGraph(State).add_sequence([retrieve, generate])
#     graph_builder.add_edge(START, "retrieve")
#     graph = graph_builder.compile()

#     response = graph.invoke(State(
#         question="许三观的身份",
#         context=[],
#         answer=""
#     ))
#     print(response["answer"])

# faiss_helper = DailyFAISSHelper(dimension=384, retention_days=7)
# faiss_helper.save_faiss_from_file()

if __name__ == "__main__":
    logger.info("启动新闻爬虫定时任务...")
    
    try:
        crawler = NewsCrawler()
        crawler.crawl_news_sites()
        faiss_helper = DailyFAISSHelper(dimension=384, retention_days=7)
        faiss_helper.save_faiss_from_json()
        faiss_helper.print_pkl_contents()
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
