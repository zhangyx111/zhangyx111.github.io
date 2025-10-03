from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db
from sqlalchemy import func, extract

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():    
    return "hello world! This is the main_bp blueprint."

@main_bp.route('/home')
def home():
    """Main_bp page"""
    return "<h1>Home Page</h1><p>Welcome to the home page!</p>"

