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
    name = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(100), nullable=False)
    is_activate = db.Column(db.Boolean, default=True)

# 用户加载器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
