from flask import Blueprint, request, jsonify
from ..services.faiss_vector import faiss_db
from flask_jwt_extended import jwt_required
import logging

llm_bp = Blueprint('llm', __name__, url_prefix="/api/llm_service")

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

@llm_bp.route('/search', methods=['GET', 'POST'])
@jwt_required()
def search():
    try:
        # 获取查询参数
        query = None
        if request.method == 'GET':
            query = request.args.get('query')
        elif request.is_json:
            data = request.get_json()
            if data:
                query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'message': '查询内容不能为空'
            }), 400
        
        # 获取搜索参数
        top_k = 5  # 默认值
        if request.method == 'GET':
            top_k = int(request.args.get('top_k', 5))
        elif request.is_json:
            data = request.get_json()
            if data:
                top_k = int(data.get('top_k', 5))
        
        # 执行搜索
        results = faiss_db.search(query, k=top_k)

        print(results)
        
        # 格式化结果
        formatted_results = []
        for i, doc in enumerate(results):
            formatted_results.append({
                'id': i + 1,
                'content': doc.page_content,
                'metadata': doc.metadata if hasattr(doc, 'metadata') else {},
                'similarity': 1.0 - (i / len(results)) if len(results) > 1 else 1.0  # 简化的相似度计算
            })
        
        return jsonify({
            'success': True,
            'message': '查询成功',
            'data': {
                'query': query,
                'results': formatted_results,
                'total': len(formatted_results)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '查询失败',
            'error': str(e)
        }), 500
