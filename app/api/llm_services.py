from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import sentence_transformers
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from typing import List, Dict, Any, Optional, Union, Tuple
from langgraph.graph import START, StateGraph
from langchain import hub
from langchain_core.embeddings import Embeddings
import datetime
from pathlib import Path
import os
from typing import Tuple
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import logging
import pickle

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log/llm_service.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('llm_service')


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
    
class LLMService:
    def __init__(self, model_name: str = "qwen3:8b"):
        """
        初始化本地LLM客户端
        
        :param model_name: 模型名称，默认为 qwen3:8b
        :param base_url: Ollama服务地址，默认为 http://localhost:11434
        """
        current_file = Path(__file__)

        self.base_dir = current_file.parent.parent.parent / "news"
        self.save_dir = os.path.join(current_file.parent.parent.parent, "instance\\faiss") 
        self.date_suffix = (str)(datetime.datetime.today().date()).replace("-", "_")
        self.retention_days = 7
        self.embedding_function = SentenceTransformerEmbeddings()
        self.faiss_dir = (str)(os.path.join(self.save_dir, f"faiss_{self.date_suffix}"))
        self.index_path = os.path.join(self.faiss_dir, "index_" + self.date_suffix + ".faiss")
        self.file_path = os.path.join(self.faiss_dir, "index_" + self.date_suffix + ".pkl")
        self.vector = None

        self.model_name = model_name
        self.llm = Ollama(
            model=model_name, 
            temperature=0.7,
            num_predict=2048
        )
        
        # 测试连接
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                print(f"成功连接到 Ollama 服务器，可用模型: {response.json()}")
            else:
                print(f"连接到 Ollama 服务器失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"无法连接到 Ollama 服务器: {str(e)}")

    def load_vector(self):
        # 将最近7天的索引合并后加载索引
        try:
            self.vector = self._merge_recent_indices(7)
            
        except Exception as e:
            logger.error(f"加载索引失败: {e}")
            raise

    def _get_faiss_paths_name(self, date: datetime.date) -> Tuple[str, str]:
        """获取指定日期的索引和元数据文件路径"""
        date_str = date.strftime("%Y_%m_%d")
        faiss_dir = os.path.join(self.save_dir, f"faiss_{date_str}")
        index_path = os.path.join(faiss_dir, f"index_{date_str}.faiss")
        file_path = os.path.join(faiss_dir, f"index_{date_str}.pkl")
        # index_name = f"index_{date_str}"
        return index_path, file_path
    
    def _merge_recent_indices(self, days: int = 7) -> FAISS:
        """
        合并最近几天的索引
        
        Args:
            days: 合并的天数
            
        Returns:
            合并后的索引和元数据
        """
        try:
            # 获取最近几天的日期
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=days-1)
            
            current_date = start_date
            merged_index = faiss.IndexFlatL2(384)
            merged_vectorstore = FAISS(
                embedding_function=self.embedding_function,
                index=merged_index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={}
            )
            
            logger.info(f"开始合并 {start_date} 到 {end_date} 的索引")
            
            while current_date <= end_date:
                # print("current_date:", current_date)
                index_path, file_path = self._get_faiss_paths_name(current_date)
                print(index_path, file_path)
                
                if os.path.exists(index_path):
                    # 读取当日索引
                    index = faiss.read_index(index_path)
    
                    # 加载文档数据
                    with open(file_path, 'rb') as f:
                        data = pickle.load(f)
                    
                    # 重新创建向量存储
                    daily_vectorstore = FAISS(
                        embedding_function=self.embedding_function,
                        index=merged_index,
                        docstore=InMemoryDocstore(),
                        index_to_docstore_id={} 
                    )
                    
                    # 恢复数据
                    daily_vectorstore.docstore._dict = data['docstore']
                    daily_vectorstore.index_to_docstore_id = data['index_to_docstore_id']
                    
                    merged_vectorstore.merge_from(daily_vectorstore)
                    
                    logger.info(f"合并 {current_date} 的索引，包含 {daily_vectorstore.index.ntotal} 个向量")

                current_date += datetime.timedelta(days=1)
            
            # 保存合并结果
            if merged_vectorstore is not None:
                merged_vectorstore.save_local(self.save_dir, index_name=f"merged_index_{current_date}days")
                logger.info(f"合并完成，总计 {daily_vectorstore.index.ntotal} 个文档")
            
                return merged_vectorstore
            else:
                logger.warning("没有找到可合并的索引，返回空索引")
                empty_index = faiss.IndexFlatL2(384)
                return FAISS(
                    embedding_function=self.embedding_function,
                    index=empty_index,
                    docstore=InMemoryDocstore({}),
                    index_to_docstore_id={},
                )
            
        except Exception as e:
            logger.error(f"合并索引失败: {e}")
            raise

    def _get_vectorstore(self):
        

    def stream(self, prompt: str):
        """
        流式调用模型
        
        :param prompt: 输入文本
        :return: 生成的文本流
        """
        try:
            for chunk in self.llm.stream(prompt):
                yield chunk
        except Exception as e:
            print(f"调用 Ollama 时发生错误: {str(e)}")
            yield ""

    





    # Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    
    improved_prompt = \
    f"""基于以下上下文回答问题。如果上下文没有相关信息，请明确说明"根据提供的资料，没有找到相关信息"。

        上下文：
        {docs_content}

        问题：{state["question"]}

        要求：
        1. 严格基于上下文信息回答
        2. 如果上下文没有相关信息，不要编造答案
        3. 如果信息不完整，请说明哪些方面缺乏信息

    回答："""
    # 修复：直接使用返回的响应
    response = llm.invoke(improved_prompt)
    
    # 简单的类型检查
    if isinstance(response, str):
        return {"answer": response}
    elif hasattr(response, 'content'):
        return {"answer": response.content}
    else:
        return {"answer": str(response)}

if __name__ == "__main__":
    
    # embedding_model = SentenceTransformerEmbeddings('sentence-transformers/all-MiniLM-L6-v2')
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # llm = Ollama(
    #     model="qwen3:8b", 
    #     temperature=0.7,
    #     num_predict=2048
    # )

    # current_file = Path(__file__)
    # news_dir = current_file.parent.parent.parent / "news"
    # index_dir = current_file.parent.parent.parent / "instance"
    # # print(f"news目录路径: {news_dir}")

    # vector_store = load_faiss_simple(embedding_model, index_dir)
    # 检查目录是否存在
    # if not os.path.isdir(news_dir):
    #     print(f"Error: Directory not found at {news_dir}")
    # else:
    #     # 遍历news目录下的所有文件
    #     for filename in os.listdir(news_dir):
    #         file_path = os.path.join(news_dir, filename)
    #         # 确保是文件而不是子目录
    #         if os.path.isfile(file_path):
    #             try:
    #                 with open(file_path, "r", encoding='utf-8') as f:
    #                     content = f.read()
                        
    #                     all_splits = text_splitter.split_text(content)
    #                     vector_store.add_texts(all_splits)

    #             except Exception as e:
    #                 print(f"Error reading file {filename}: {e}")

    
    # save_faiss_simple(vector_store, index_dir)

    # 查看向量存储的基本信息
    # print(f"向量数量: {vector_store.index.ntotal}")
    # print(f"向量维度: {vector_store.index.d}")

    # # 查看索引到文档的映射
    # print(f"索引映射数量: {len(vector_store.index_to_docstore_id)}")

    llm_service = LLMService()
    vector_store = llm_service.load_vector()
    llm = llm_service.llm

    

    prompt = hub.pull("rlm/rag-prompt")

    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    response = graph.invoke(State(
        question="许三观的身份",
        context=[],
        answer=""
    ))
    print(response["answer"])
    
    
    
