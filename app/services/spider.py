from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import os
import numpy as np
import glob

from langchain.schema import Document
from bs4 import BeautifulSoup
import feedparser
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

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
                        'crawled_at': datetime.datetime.now().isoformat()
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
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

        # 确保基础目录存在
        try:
            if os.path.exists(self.base_dir) is False:
                logger.warning("新闻目录不存在，无法初始化DailyFAISSHelper")

            if os.path.exists(self.faiss_dir) is False:
                os.makedirs(self.faiss_dir, exist_ok=True)
                logger.info(f"创建索引保存目录: {self.faiss_dir}")

        except Exception as e:
            logger.error("初始化失败")
        
        logger.info(f"初始化DailyFAISSHelper，基础目录: {self.base_dir}, 维度: {dimension}, 保留天数: {retention_days}")
    
    def save_faiss_from_txt(self):
        success = False
        documents_processed = False
        
        try:
            # 处理数据部分
            txt_file_path = self.base_dir / self.date_suffix / f"news_{self.date_suffix}.txt"
            
            if not os.path.exists(txt_file_path):
                logger.warning(f"新闻txt文件不存在: {txt_file_path}")
                return False
            
            with open(txt_file_path, 'r', encoding='utf-8') as f:
                news_data = f.read()
                all_splits = self.text_splitter.split_text(news_data)
                self.vector.add_texts(all_splits)
            
            
            logger.info(f"从 {txt_file_path} 加载了 {self.vector.index.ntotal} 条新闻")            
            documents_processed = True
            
        except Exception as e:
            logger.error(f"处理新闻数据时出错: {e}")
            # 即使处理出错，也尝试保存当前状态
            documents_processed = True
        
        # 无论前面是否出错，只要处理了文档就尝试保存
        if documents_processed:
            try:                
                # 保存索引
                logger.info(f"保存索引到: {self.index_path}")
                faiss.write_index(self.vector.index, str(self.index_path))
                
                # 保存文档数据
                logger.info(f"保存文档数据到: {self.file_path}")
                with open(self.file_path, 'wb') as f:
                    pickle.dump({
                        'docstore': self.vector.docstore._dict,
                        'index_to_docstore_id': self.vector.index_to_docstore_id
                    }, f)
                
                logger.info(f"保存成功到: {self.faiss_dir}")
                success = True
                
            except Exception as e:
                logger.error(f"保存FAISS索引失败: {e}")
                success = False
        
        return success

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

    
    
    



# faiss_helper = DailyFAISSHelper(dimension=384, retention_days=7)
# faiss_helper.save_faiss_from_file()

if __name__ == "__main__":
    logger.info("启动新闻爬虫定时任务...")
    
    try:
        # crawler = NewsCrawler()
        # crawler.crawl_news_sites()
        faiss_helper = DailyFAISSHelper(dimension=384, retention_days=7)
        faiss_helper.save_faiss_from_txt()
        faiss_helper.print_pkl_contents()
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
