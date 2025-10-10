from flask import Blueprint, request, jsonify

llm_bp = Blueprint('llm', __name__, url_prefix="/api/llm_service")

@llm_bp.route('/search')
def search():
    request.get_data()

    return jsonify({
            'success': False,
            'message': '获取知识库列表失败',
            'error': str(123)
        }), 500