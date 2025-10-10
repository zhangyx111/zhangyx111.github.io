from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime
import uuid

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    def __init__(self, name, email) -> None:
        super().__init__()
        self.username = name
        self.email = email

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# 知识库条目表
class KnowledgeItem(db.Model):
    __tablename__ = 'knowledge_items'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    source = db.Column(db.String(100))
    source_url = db.Column(db.String(500))
    category = db.Column(db.String(50))
    file_type = db.Column(db.String(20), default='text')  # text, pdf, doc, image, etc.
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_processed = db.Column(db.Boolean, default=False)
    item_metadata = db.Column(db.JSON)
    
    # 关联关系
    creator = db.relationship('User', backref='knowledge_items')
    tags = db.relationship('Tag', secondary='knowledge_tags', backref='knowledge_items')
    
    def __repr__(self):
        return f'<KnowledgeItem {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'source': self.source,
            'source_url': self.source_url,
            'category': self.category,
            'file_type': self.file_type,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by,
            'is_processed': self.is_processed,
            'metadata': self.item_metadata,
            'tags': [tag.to_dict() for tag in self.tags]
        }

# 标签表
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#007bff')  # 十六进制颜色
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# 知识库标签关联表
class KnowledgeTag(db.Model):
    __tablename__ = 'knowledge_tags'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    knowledge_id = db.Column(db.String(36), db.ForeignKey('knowledge_items.id'), nullable=False)
    tag_id = db.Column(db.String(36), db.ForeignKey('tags.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 防止重复关联
    __table_args__ = (db.UniqueConstraint('knowledge_id', 'tag_id'),)

# 用户加载器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
