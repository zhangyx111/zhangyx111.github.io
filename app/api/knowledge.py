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

@knowledge_bp.route('/upload', methods=['POST'])
# @jwt_required()
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
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '文件添加成功',
            'data': knowledge_item.name,
            'tag':True
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"添加知识库文件失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '添加知识库文件失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/delete/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_knowledge_file(id):
    pass

# @knowledge_bp.route('/import', methods=['POST'])
# @jwt_required()
