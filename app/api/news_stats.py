import os
from flask import Blueprint, jsonify
from pathlib import Path
import json
from datetime import datetime, timedelta

news_stats_bp = Blueprint('news_stats', __name__)

@news_stats_bp.route('/api/news/count', methods=['GET'])
def get_news_count():
    """获取新闻总数"""
    try:
        # 尝试从环境变量获取（如果spider.py运行过）
        news_count = os.environ.get("NewsCount")
        if news_count and news_count.isdigit():
            return jsonify({"count": int(news_count)})
        
        # 如果环境变量中没有，则计算news目录中的新闻数量
        news_dir = Path(__file__).parent.parent.parent / "news"
        if not news_dir.exists():
            return jsonify({"count": 0})
        
        total_count = 0
        # 统计最近7天的新闻文件
        date_threshold = datetime.now() - timedelta(days=7)
        
        for file_path in news_dir.glob("news_*.json"):
            try:
                # 检查文件是否在最近7天内
                file_date_str = file_path.stem.replace("news_", "")
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
                
                if file_date >= date_threshold:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        news_data = json.load(f)
                        total_count += len(news_data)
            except Exception as e:
                # 忽略无法解析的文件
                continue
        
        return jsonify({"count": total_count})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
