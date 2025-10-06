from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import requests
import time
import statistics
import datetime
from pathlib import Path
import os
from .spider import SentenceTransformerEmbeddings

from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import logging

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

class LLMService:
    def __init__(self, model_name: str = "qwen3:8b"):
        """
        初始化本地LLM客户端
        
        :param model_name: 模型名称，默认为 qwen3:8b
        :param base_url: Ollama服务地址，默认为 http://localhost:11434
        """
        current_file = Path(__file__)

        self.base_dir = current_file.parent.parent.parent / "news"
        self.save_dir = current_file.parent.parent.parent / "instance" / "faiss"
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
        index_name = f"index_{date_str}"
        return faiss_dir, index_name
    
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
            merged_index = faiss.IndexFlatL2(self.dimension)
            merged_vectorstore = None
            
            logger.info(f"开始合并 {start_date} 到 {end_date} 的索引")
            
            while current_date <= end_date:
                # print("current_date:", current_date)
                faiss_path, index_name = self._get_faiss_paths_name(current_date)
                
                if os.path.exists(faiss_path):
                    # 读取当日索引
                    daily_vectorstore = FAISS.load_local(
                        faiss_path,
                        self.embedding_function, 
                        index_name, 
                        allow_dangerous_deserialization=True
                    )
                    
                   # 首次直接使用，后续合并
                    if merged_vectorstore is None:
                        merged_vectorstore = daily_vectorstore
                    else:
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
                empty_index = faiss.IndexFlatL2(self.dimension)
                return FAISS(
                    embedding_function=self.embedding_function,
                    index=empty_index,
                    docstore=InMemoryDocstore({}),
                    index_to_docstore_id={},
                )
            
        except Exception as e:
            logger.error(f"合并索引失败: {e}")
            raise

    def cleanup_old_data(self) -> int:
        """
        清理过期数据
        
        Returns:
            删除的索引文件数量
        """
        try:
            cutoff_date = datetime.date.today() - datetime.timedelta(days=self.retention_days)
            logger.info(f"清理早于 {cutoff_date} 的数据")
            deleted_count = 0
            
            # 获取 save_dir 下的所有子文件夹
            if not os.path.exists(self.save_dir):
                logger.warning(f"保存目录不存在: {self.save_dir}")
                return 0
            
            all_items = os.listdir(self.save_dir)
            
            for item_name in all_items:
                item_path = os.path.join(self.save_dir, item_name)
                print(item_name)
                # 只处理文件夹
                if not os.path.isdir(item_path):
                    continue
            
                if item_name.startswith("faiss_"):
                    date_str = item_name[6:]  # 去掉 "faiss"
                    print(date_str, len(date_str))
                    if len(date_str) == 10 and date_str.count('_') == 2:
                        try:
                            file_date = datetime.datetime.strptime(date_str, "%Y_%m_%d").date()
                            print(file_date)
                        except ValueError:
                            logger.warning(f"无法解析日期: {date_str}")
            
                # 如果成功解析日期且日期早于截止日期，删除文件夹
                if file_date is not None and file_date <= cutoff_date:
                    try:
                        import shutil
                        shutil.rmtree(item_path)
                        deleted_count += 1
                        logger.info(f"删除过期文件夹: {item_name} (创建日期: {file_date})")
                    except Exception as e:
                        logger.error(f"删除文件夹失败: {item_name}, 错误: {e}")
            
            logger.info(f"清理完成，删除了 {deleted_count} 个过期的索引文件")
            return deleted_count
            
        except Exception as e:
            logger.error(f"清理数据失败: {e}")
            raise

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

    



# 使用示例
if __name__ == "__main__":
    
    # 测试 SentenceTransformer 和 Ollama embedding 模型的速度

    reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
    scores = reranker_model.predict([
        ("How many people live in Berlin?", "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers."),
        ("How many people live in Berlin?", "Berlin is well known for its museums."),
        ])
    print(scores)
    
    
    
    
