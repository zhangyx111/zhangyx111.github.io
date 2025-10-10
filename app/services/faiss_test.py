import os
import re
import faiss
from langchain_community.vectorstores import FAISS
from typing_extensions import List
import sentence_transformers
from langchain_core.embeddings import Embeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

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

class LangChainFAISSDynamic:
    def __init__(self, index_path="faiss_index", embedding_model=None):
        self.index_path = index_path
        self.embeddings = SentenceTransformerEmbeddings()
        
        # 尝试加载现有索引，否则创建空索引
        if os.path.exists(index_path):
            self.vector_store = FAISS.load_local(
                index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            # 创建空索引
            self.vector_store = FAISS.from_texts(
                [""],  # 初始空文档
                self.embeddings
            )
            # 立即移除空文档
            self._recreate_without_initial()
    
    def _recreate_without_initial(self):
        """重新创建没有初始空文档的索引"""
        # 这是一个workaround，因为FAISS不能直接创建空索引
        pass
    
    def _get_optimized_splitter(self, file_extension):
        """根据文件类型返回优化的文本分割器"""
        
        # 基础分割器配置
        base_config = {
            "chunk_size": 800,  # 稍微减小块大小
            "chunk_overlap": 150,
            "length_function": len,
        }
        
        # 针对不同文件类型优化分隔符
        if file_extension == '.txt':
            # 文本文件：使用更细粒度的分隔符
            return RecursiveCharacterTextSplitter(
                separators=[
                    "\n\n", "\n", "。", "！", "？", "；", "，", " ", ""  # 中文标点支持
                ],
                **base_config
            )
        elif file_extension == '.pdf':
            # PDF文件：保持段落结构
            return RecursiveCharacterTextSplitter(
                separators=[
                    "\n\n", "\n", "。", "！", "？", ". ", "! ", "? ", " ", ""
                ],
                **base_config
            )
        else:
            # 默认分割器
            return RecursiveCharacterTextSplitter(**base_config)

    def _preprocess_text(self, text, filename):
        """预处理文本，处理超长行和特殊格式"""
        
        # 处理超长行（无换行符的文本）
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            if len(line) > 2000:  # 如果单行超过2000字符，强制分割
                # 按句子分割（中文支持）
                sentences = re.split(r'[。！？；.!?;]', line)
                current_chunk = ""
                
                for sentence in sentences:
                    if sentence.strip():  # 跳过空句子
                        if len(current_chunk + sentence) > 800:
                            if current_chunk:
                                processed_lines.append(current_chunk.strip())
                            current_chunk = sentence
                        else:
                            current_chunk += sentence
                
                if current_chunk:
                    processed_lines.append(current_chunk.strip())
            else:
                processed_lines.append(line)
        
        # 重新组合文本
        processed_text = '\n'.join(processed_lines)
        
        # 移除过多的空白字符
        processed_text = re.sub(r'\n\s*\n', '\n\n', processed_text)
        
        print(f"预处理完成: {filename}, 原始长度: {len(text)}, 处理后: {len(processed_text)}")
        return processed_text

    def add_file(self, file_path):
        """添加单个文件到索引"""
        # 根据文件类型选择加载器
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        elif ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext in ['.doc', '.docx']:
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        # 加载文档
        documents = loader.load()
        
        all_splits = []
        for i, doc in enumerate(documents):
            print(f"处理第 {i+1} 页, 长度: {len(doc.page_content)} 字符")
            
            # 预处理文本
            processed_content = self._preprocess_text(doc.page_content, os.path.basename(file_path))
            
            # 获取合适的分割器
            text_splitter = RecursiveCharacterTextSplitter()
            
            # 分割文本
            all_splits = text_splitter.split_text(processed_content)
        
        
            # 创建临时索引并合并
            if all_splits:
                temp_store = FAISS.from_texts(all_splits, self.embeddings)
                self.vector_store.merge_from(temp_store)
                
                print(f"✅ 成功添加文件: {file_path}, 新增 {len(all_splits)} 个文档块")
                print(f"当前索引总块数: {self.vector_store.index.ntotal}")
                return True
            else:
                print(f"❌ 文件 {file_path} 没有生成任何有效的文本块")
                return False
    
    def add_directory(self, directory_path):
        """批量添加目录中的所有文件"""
        supported_extensions = ['.txt', '.pdf', '.doc', '.docx']
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in supported_extensions:
                    try:
                        self.add_file(file_path)
                    except Exception as e:
                        print(f"处理文件 {filename} 时出错: {str(e)}")
    
    def add_texts(self, texts, metadatas=None):
        """直接添加文本"""
        temp_store = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        self.vector_store.merge_from(temp_store)
    
    def save(self):
        """保存索引"""
        self.vector_store.save_local(self.index_path)
    
    def search(self, query, k=5):
        """搜索"""
        return self.vector_store.similarity_search(query, k=k)
    
    def get_doc_count(self):
        """获取文档数量"""
        return self.vector_store.index.ntotal

faiss_db = LangChainFAISSDynamic()

# # 使用示例
# if __name__ == "__main__":
#     # 初始化
#     faiss_manager = LangChainFAISSDynamic("my_knowledge_base")
    
#     # 添加单个文件
#     # faiss_manager.add_file("document1.pdf")
    
#     # 添加多个文件
#     # faiss_manager.add_directory("knowledge_docs")

#     faiss_manager.add_file("news\huozhe.txt")
    
#     # 搜索
#     results = faiss_manager.search("人工智能")
#     for i, doc in enumerate(results):
#         print(f"结果 {i+1}: {doc.page_content[:100]}...")
    
#     # 保存索引
#     faiss_manager.save()
    
#     print(f"总文档块数量: {faiss_manager.get_doc_count()}")

