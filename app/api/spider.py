from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import os

import bs4
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

def save_faiss_simple(vector_store, save_dir):
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存索引
    faiss.write_index(vector_store.index, str(save_dir / "index.faiss"))
    
    # 保存文档数据
    with open(save_dir / "docstore.pkl", 'wb') as f:
        pickle.dump({
            'docstore': vector_store.docstore._dict,
            'index_to_docstore_id': vector_store.index_to_docstore_id
        }, f)
    
    print(f"保存成功到: {save_dir}")

def load_faiss_simple(embedding_function, save_dir):
    save_dir = Path(save_dir)
    
    # 加载索引
    index = faiss.read_index(str(save_dir / "index.faiss"))
    
    # 加载文档数据
    with open(save_dir / "docstore.pkl", 'rb') as f:
        data = pickle.load(f)
    
    # 重新创建向量存储
    vector_store = FAISS(
        embedding_function=embedding_function,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
    # 恢复数据
    vector_store.docstore._dict = data['docstore']
    vector_store.index_to_docstore_id = data['index_to_docstore_id']
    
    print(f"加载成功，包含 {vector_store.index.ntotal} 个向量")
    return vector_store

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

class State(TypedDict):
        question: str
        context: List[Document]
        answer: str


    # Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


# 只修改 generate 函数
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
    
    embedding_model = SentenceTransformerEmbeddings('sentence-transformers/all-MiniLM-L6-v2')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    llm = Ollama(
        model="qwen3:8b", 
        temperature=0.7,
        num_predict=2048
    )

    
    # vector_store = FAISS(
    #     embedding_function = embedding_model,
    #     index = faiss.IndexFlatL2(384),  # 384 is the dimension for all-MiniLM-L6-v2
    #     docstore=InMemoryDocstore(),
    #     index_to_docstore_id={},
    # )

    current_file = Path(__file__)
    news_dir = current_file.parent.parent.parent / "news"
    index_dir = current_file.parent.parent.parent / "instance"
    # print(f"news目录路径: {news_dir}")

    vector_store = load_faiss_simple(embedding_model, index_dir)
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
    print(f"向量数量: {vector_store.index.ntotal}")
    print(f"向量维度: {vector_store.index.d}")

    # 查看索引到文档的映射
    print(f"索引映射数量: {len(vector_store.index_to_docstore_id)}")

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

    # faiss.write_index(faiss.IndexFlatL2(384), os.path.join(index_dir, "faiss.index"))
    
    # print(f"索引和元数据已保存到 {index_dir} 目录")

    
