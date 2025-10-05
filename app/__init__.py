import os
import logging
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
jwt = JWTManager()

@login_manager.user_loader
def load_user(user_id):
    """从用户ID加载用户"""
    from .models import User  # 避免循环导入
    return User.query.get(int(user_id))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    CORS(app, resources={r"/auth/*": {"origins": app.config['CORS_ORIGINS']}})

    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints first (API routes take precedence)
    from app.main.views import main_bp
    app.register_blueprint(main_bp, static_folder='static', template_folder='templates')

    from app.auth.views import auth_bp
    app.register_blueprint(auth_bp, url_prefix = "/auth", static_folder='static', template_folder='templates')
    
    return app

# Import models to ensure they are registered with SQLAlchemy
from app import models
