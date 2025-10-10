from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from app import db
from app.models import KnowledgeItem, Tag, KnowledgeTag, User
from app.utils.file_utils import allowed_file, get_file_size, save_uploaded_file
from flask_jwt_extended import get_jwt, get_jwt_identity

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')

@knowledge_bp.route('', methods=['GET'])
@jwt_required()
def get_knowledge_items():
    """获取知识库列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        source = request.args.get('source')
        tag_id = request.args.get('tag_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        search = request.args.get('search')
        
        # 构建查询
        query = KnowledgeItem.query
        
        # 应用筛选条件
        if category:
            query = query.filter(KnowledgeItem.category == category)
        
        if source:
            query = query.filter(KnowledgeItem.source == source)
        
        if tag_id:
            query = query.join(KnowledgeTag).filter(KnowledgeTag.tag_id == tag_id)
        
        if start_date:
            start_date = datetime.fromisoformat(start_date)
            query = query.filter(KnowledgeItem.created_at >= start_date)
        
        if end_date:
            end_date = datetime.fromisoformat(end_date)
            query = query.filter(KnowledgeItem.created_at <= end_date)
        
        if search:
            query = query.filter(
                (KnowledgeItem.title.contains(search)) |
                (KnowledgeItem.content.contains(search)) |
                (KnowledgeItem.summary.contains(search))
            )
        
        # 获取当前用户
        current_user_id = get_jwt_identity()
        user_info = get_jwt()
        is_admin = user_info.get('is_admin', False) if user_info else False
        if not is_admin:
            query = query.filter(KnowledgeItem.created_by == current_user_id)
        
        # 分页查询
        pagination = query.order_by(KnowledgeItem.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        items = [item.to_dict() for item in pagination.items]
        
        return jsonify({
            'success': True,
            'data': {
                'items': items,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"获取知识库列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取知识库列表失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('', methods=['POST'])
@jwt_required()
def create_knowledge_item():
    """创建知识库条目"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'缺少必填字段: {field}'
                }), 400
        
        # 创建知识库条目
        knowledge_item = KnowledgeItem(
            title=data['title'],
            content=data['content'],
            summary=data.get('summary', ''),
            source=data.get('source'),
            source_url=data.get('source_url'),
            category=data.get('category'),
            publish_date=datetime.fromisoformat(data['publish_date']) if data.get('publish_date') else None,
            created_by=current_user_id,
            metadata=data.get('metadata', {})
        )
        
        # 添加标签
        if 'tags' in data:
            for tag_name in data['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()
                
                if tag not in knowledge_item.tags:
                    knowledge_item.tags.append(tag)
        
        db.session.add(knowledge_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '知识库条目创建成功',
            'data': knowledge_item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建知识库条目失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '创建知识库条目失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
def update_knowledge_item(id):
    """更新知识库条目"""
    try:
        current_user_id = get_jwt_identity()
        knowledge_item = KnowledgeItem.query.get_or_404(id)
        
        # 检查权限
        user_info = get_jwt()
        is_admin = user_info.get('is_admin', False) if user_info else False
        if not is_admin and knowledge_item.created_by != current_user_id:
            return jsonify({
                'success': False,
                'message': '没有权限修改此条目'
            }), 403
        
        data = request.get_json()
        
        # 更新字段
        if 'title' in data:
            knowledge_item.title = data['title']
        if 'content' in data:
            knowledge_item.content = data['content']
        if 'summary' in data:
            knowledge_item.summary = data['summary']
        if 'source' in data:
            knowledge_item.source = data['source']
        if 'source_url' in data:
            knowledge_item.source_url = data['source_url']
        if 'category' in data:
            knowledge_item.category = data['category']
        if 'publish_date' in data:
            knowledge_item.publish_date = datetime.fromisoformat(data['publish_date']) if data['publish_date'] else None
        if 'metadata' in data:
            knowledge_item.metadata = data['metadata']
        
        # 更新标签
        if 'tags' in data:
            # 清除现有标签
            knowledge_item.tags.clear()
            
            # 添加新标签
            for tag_name in data['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()
                
                    if tag not in knowledge_item.tags:
                        knowledge_item.tags.append(tag)
        
        knowledge_item.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '知识库条目更新成功',
            'data': knowledge_item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新知识库条目失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '更新知识库条目失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_knowledge_item(id):
    """删除知识库条目"""
    try:
        current_user_id = get_jwt_identity()
        knowledge_item = KnowledgeItem.query.get_or_404(id)
        
        # 检查权限
        user_info = get_jwt()
        is_admin = user_info.get('is_admin', False) if user_info else False
        if not is_admin and knowledge_item.created_by != current_user_id:
            return jsonify({
                'success': False,
                'message': '没有权限删除此条目'
            }), 403
        
        # 删除文件
        if knowledge_item.file_path and os.path.exists(knowledge_item.file_path):
            os.remove(knowledge_item.file_path)
        
        db.session.delete(knowledge_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '知识库条目删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除知识库条目失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '删除知识库条目失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/batch', methods=['DELETE'])
@jwt_required()
def batch_delete_knowledge_items():
    """批量删除知识库条目"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        item_ids = data.get('ids', [])
        
        if not item_ids:
            return jsonify({
                'success': False,
                'message': '请选择要删除的条目'
            }), 400
        
        # 获取要删除的条目
        query = KnowledgeItem.query.filter(KnowledgeItem.id.in_(item_ids))
        user_info = get_jwt()
        is_admin = user_info.get('is_admin', False) if user_info else False
        if not is_admin:
            query = query.filter(KnowledgeItem.created_by == current_user_id)
        
        items = query.all()
        
        if not items:
            return jsonify({
                'success': False,
                'message': '未找到指定的条目'
            }), 404
        
        # 删除文件和数据库记录
        for item in items:
            if item.file_path and os.path.exists(item.file_path):
                os.remove(item.file_path)
            db.session.delete(item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'成功删除 {len(items)} 个条目'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除知识库条目失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '批量删除知识库条目失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_knowledge_file():
    """上传文件到知识库"""
    try:
        current_user_id = get_jwt_identity()
        
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        if file and allowed_file(file.filename):
            # 安全的文件名
            filename = secure_filename(file.filename or '')
            file_extension = filename.rsplit('.', 1)[1].lower() if filename else ''
            
            # 生成唯一文件名
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'knowledge', unique_filename)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 保存文件
            file.save(file_path)
            
            # 获取文件信息
            file_size = get_file_size(file_path)
            
            # 创建知识库条目
            title = request.form.get('title', filename)
            content = request.form.get('content', '')
            summary = request.form.get('summary', '')
            source = request.form.get('source')
            category = request.form.get('category')
            publish_date = request.form.get('publish_date')
            
            knowledge_item = KnowledgeItem(
                title=title,
                content=content,
                summary=summary,
                source=source,
                category=category,
                file_type=file_extension,
                file_path=file_path,
                file_size=file_size,
                publish_date=datetime.fromisoformat(publish_date) if publish_date else None,
                created_by=current_user_id,
                metadata={
                    'original_filename': filename,
                    'mime_type': file.mimetype
                }
            )
            
            # 添加标签
            if 'tags' in request.form:
                tags = request.form['tags'].split(',')
                for tag_name in tags:
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag = Tag.query.filter_by(name=tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            db.session.add(tag)
                            db.session.flush()
                        
                        if tag not in knowledge_item.tags:
                            knowledge_item.tags.append(tag)
            
            db.session.add(knowledge_item)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': '文件上传成功',
                'data': knowledge_item.to_dict()
            }), 201
        
        return jsonify({
            'success': False,
            'message': '不支持的文件类型'
        }), 400
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"文件上传失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '文件上传失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/download/<string:id>')
@jwt_required()
def download_knowledge_file(id):
    """下载知识库文件"""
    try:
        current_user_id = get_jwt_identity()
        knowledge_item = KnowledgeItem.query.get_or_404(id)
        
        # 检查权限
        user_info = get_jwt()
        is_admin = user_info.get('is_admin', False) if user_info else False
        if not is_admin and knowledge_item.created_by != current_user_id:
            return jsonify({
                'success': False,
                'message': '没有权限下载此文件'
            }), 403
        
        if not knowledge_item.file_path or not os.path.exists(knowledge_item.file_path):
            return jsonify({
                'success': False,
                'message': '文件不存在'
            }), 404
        
        directory = os.path.dirname(knowledge_item.file_path)
        filename = os.path.basename(knowledge_item.file_path)
        
        return send_file(
            knowledge_item.file_path,
            as_attachment=True,
            download_name=knowledge_item.metadata.get('original_filename', filename)
        )
        
    except Exception as e:
        current_app.logger.error(f"文件下载失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '文件下载失败',
            'error': str(e)
        }), 500

# 标签管理API
@knowledge_bp.route('/tags', methods=['GET'])
@jwt_required()
def get_tags():
    """获取标签列表"""
    try:
        tags = Tag.query.order_by(Tag.name).all()
        return jsonify({
            'success': True,
            'data': [tag.to_dict() for tag in tags]
        })
    except Exception as e:
        current_app.logger.error(f"获取标签列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取标签列表失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/tags', methods=['POST'])
@jwt_required()
def create_tag():
    """创建标签"""
    try:
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({
                'success': False,
                'message': '标签名称不能为空'
            }), 400
        
        # 检查标签是否已存在
        existing_tag = Tag.query.filter_by(name=data['name']).first()
        if existing_tag:
            return jsonify({
                'success': False,
                'message': '标签已存在'
            }), 400
        
        tag = Tag(
            name=data['name'],
            description=data.get('description', ''),
            color=data.get('color', '#007bff')
        )
        
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '标签创建成功',
            'data': tag.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建标签失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '创建标签失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/tags/<string:id>', methods=['PUT'])
@jwt_required()
def update_tag(id):
    """更新标签"""
    try:
        tag = Tag.query.get_or_404(id)
        data = request.get_json()
        
        if 'name' in data:
            # 检查新名称是否与其他标签冲突
            existing_tag = Tag.query.filter(Tag.name == data['name'], Tag.id != id).first()
            if existing_tag:
                return jsonify({
                    'success': False,
                    'message': '标签名称已存在'
                }), 400
            tag.name = data['name']
        
        if 'description' in data:
            tag.description = data['description']
        
        if 'color' in data:
            tag.color = data['color']
        
        tag.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '标签更新成功',
            'data': tag.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新标签失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '更新标签失败',
            'error': str(e)
        }), 500

@knowledge_bp.route('/tags/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_tag(id):
    """删除标签"""
    try:
        tag = Tag.query.get_or_404(id)
        
        # 检查是否有关联的知识库条目
        if tag.knowledge_items:
            return jsonify({
                'success': False,
                'message': '该标签下还有知识库条目，无法删除'
            }), 400
        
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '标签删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除标签失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '删除标签失败',
            'error': str(e)
        }), 500
