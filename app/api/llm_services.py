from langchain_community.llms import Ollama
#from langchain_community.embeddings import OllamaEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import requests
import time
import statistics

from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
scores = reranker_model.predict([
    ("How many people live in Berlin?", "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers."),
    ("How many people live in Berlin?", "Berlin is well known for its museums."),
])
print(scores)
# [ 8.607138 -4.320078]

sentences = ["This is an example sentence", "Each sentence is converted"]

embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = embeddings_model.encode(sentences)
print(embeddings)

# vector_store = FAISS(
#     embedding_function=embeddings,
#     index=index,
#     docstore=InMemoryDocstore(),
#     index_to_docstore_id={},
# )    

class LLMService:
    def __init__(self, model_name: str = "qwen3:8b"):
        """
        初始化本地LLM客户端
        
        :param model_name: 模型名称，默认为 qwen3:8b
        :param base_url: Ollama服务地址，默认为 http://localhost:11434
        """
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

    

def compare_embedding_models(model1, model2, sentences, num_times: int = 5):
    """
    比较两个嵌入模型的响应时间
    
    :param model1: 第一个嵌入模型
    :param model2: 第二个嵌入模型
    :param sentences: 测试句子列表
    :param num_times: 每个模型的调用次数
    :return: 比较结果
    """
    results = {}
    
    # 测试模型1
    print("\n正在测试模型1: SentenceTransformer")
    times1 = []
    for _ in range(num_times):
        start_time = time.time()
        try:
            embeddings = model1.encode(sentences)
            end_time = time.time()
            generation_time = end_time - start_time
            times1.append(generation_time)
        except Exception as e:
            print(f"调用模型1时发生错误: {str(e)}")
            times1.append(float('inf'))
    
    valid_times1 = [t for t in times1 if t != float('inf')]
    if valid_times1:
        avg_time1 = statistics.mean(valid_times1)
        median_time1 = statistics.median(valid_times1)
        min_time1 = min(valid_times1)
        max_time1 = max(valid_times1)
        
        results['SentenceTransformer'] = {
            'avg_time': avg_time1,
            'median_time': median_time1,
            'min_time': min_time1,
            'max_time': max_time1,
            'times': valid_times1
        }
        print(f"模型1测试完成:")
        print(f"  平均时间: {avg_time1:.2f}秒")
        print(f"  中位数时间: {median_time1:.2f}秒")
        print(f"  最小时间: {min_time1:.2f}秒")
        print(f"  最大时间: {max_time1:.2f}秒")
    else:
        print("模型1所有测试均失败")
        results['SentenceTransformer'] = None
    
    # 测试模型2
    print("\n正在测试模型2: Ollama embedding")
    times2 = []
    for _ in range(num_times):
        start_time = time.time()
        try:
            embeddings = model2.embed_query(sentences)  # 这可能需要根据实际API调整
            end_time = time.time()
            generation_time = end_time - start_time
            times2.append(generation_time)
        except Exception as e:
            print(f"调用模型2时发生错误: {str(e)}")
            times2.append(float('inf'))
    
    valid_times2 = [t for t in times2 if t != float('inf')]
    if valid_times2:
        avg_time2 = statistics.mean(valid_times2)
        median_time2 = statistics.median(valid_times2)
        min_time2 = min(valid_times2)
        max_time2 = max(valid_times2)
        
        results['Ollama'] = {
            'avg_time': avg_time2,
            'median_time': median_time2,
            'min_time': min_time2,
            'max_time': max_time2,
            'times': valid_times2
        }
        print(f"模型2测试完成:")
        print(f"  平均时间: {avg_time2:.2f}秒")
        print(f"  中位数时间: {median_time2:.2f}秒")
        print(f"  最小时间: {min_time2:.2f}秒")
        print(f"  最大时间: {max_time2:.2f}秒")
    else:
        print("模型2所有测试均失败")
        results['Ollama'] = None
    
    # 找出最快的模型
    if results:
        fastest_model = min(
            [(name, data) for name, data in results.items() if data is not None],
            key=lambda x: x[1]['avg_time']
        )
        print(f"\n最快的嵌入模型是: {fastest_model[0]}, 平均时间: {fastest_model[1]['avg_time']:.2f}秒")
    
    return results

# 使用示例
if __name__ == "__main__":
    
    # 测试 SentenceTransformer 和 Ollama embedding 模型的速度

    reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
    scores = reranker_model.predict([
        ("How many people live in Berlin?", "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers."),
        ("How many people live in Berlin?", "Berlin is well known for its museums."),
        ])
    print(scores)
    
    
    
    
