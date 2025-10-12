from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os
import uuid
import shutil
from werkzeug.utils import secure_filename
from app import db
from app.models import KnowledgeItem, User
from app.utils.file_utils import allowed_file, get_file_size, save_uploaded_file
from pathlib import Path
import pickle
import numpy as np
from .llm_service import faiss_db

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')

@knowledge_bp.route('/', methods=['GET'])
@jwt_required()
def get_knowledge_items():
    """获取知识库列表"""
    try:
        knowledge_items = KnowledgeItem.query.all()
        
        return jsonify({
            'success': True,
            'data': {
                'items': [{
                    'id': item.id,
                    'name': item.name,
                    'path': item.path,
                    'is_activate': item.is_activate
                } for item in knowledge_items],
                'total': len(knowledge_items),
                'pages': 1,
                'current_page': 1
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"获取知识库列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取知识库列表失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/upload', methods=['POST'])
@jwt_required()
def add_knowledge_file():
    """添加知识库文件并进行向量化"""
    try:
        # 检查文件是否在请求中
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': '没有上传文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': '未选择文件'
            }), 400
        
        # 获取其他表单数据
        data = request.form
        file_name = data.get('file_name', file.filename)
        
        # 创建上传目录
        upload_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', './uploads'))
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_dir, str(file_name))
        file.save(file_path)
        
        # 创建知识库条目
        knowledge_item = KnowledgeItem(
            name=file_name,
            path=file_path,
        )
        
        db.session.add(knowledge_item)
        db.session.flush()
        
        # 处理文件向量化
        try:
            faiss_db.add_file(file_path=file_path)
            db.session.commit()
            
        except Exception as vector_error:
            current_app.logger.error(f"文件向量化失败: {str(vector_error)}")
            # 如果向量化失败，删除已保存的文件和数据库记录
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(knowledge_item)
                db.session.commit()
            except Exception as cleanup_error:
                current_app.logger.error(f"清理失败: {str(cleanup_error)}")
                db.session.rollback()
            return jsonify({
                'success': False,
                'message': '文件向量化失败',
                'error': str(vector_error)
            }), 422
        
        return jsonify({
            'success': True,
            'message': '文件添加成功',
            'data': knowledge_item.name
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"添加知识库文件失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '添加知识库文件失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/<string:name>', methods=['PUT'])
@jwt_required()
def update_knowledge_file(name):
    """更新知识库条目"""
    try:
        knowledge_item = KnowledgeItem.query.filter_by(name=name).first()
        if not knowledge_item:
            return jsonify({
                'success': False,
                'message': '知识库条目不存在'
            }), 404
        
        data = request.get_json()
        
        # 更新字段
        if 'name' in data:
            knowledge_item.name = data['name']
        if 'is_activate' in data:
            knowledge_item.is_activate = data['is_activate']
        
        knowledge_item.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '知识库条目更新成功',
            'data': {
                'id': knowledge_item.id,
                'name': knowledge_item.name,
                'path': knowledge_item.path,
                'is_activate': knowledge_item.is_activate,
                'updated_at': knowledge_item.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新知识库条目失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '更新知识库条目失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_knowledge_file(name):
    """删除知识库条目"""
    try:
        knowledge_item = KnowledgeItem.query.filter_by(name=name).first()
        if not knowledge_item:
            return jsonify({
                'success': False,
                'message': '知识库条目不存在'
            }), 404
        
        # 删除关联的文件
        if os.path.exists(knowledge_item.path):
            try:
                os.remove(knowledge_item.path)
                current_app.logger.info(f"已删除文件: {knowledge_item.path}")
            except Exception as file_error:
                current_app.logger.warning(f"删除文件失败: {knowledge_item.path}, 错误: {str(file_error)}")
        
        # 从数据库中删除记录
        db.session.delete(knowledge_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '知识库条目删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除知识库条目失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '删除知识库条目失败',
            'error': str(e)
        }), 500
