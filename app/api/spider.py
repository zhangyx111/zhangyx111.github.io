from flask import jsonify, Blueprint
from ..services.spider import NewsCrawler, DailyFAISSHelper

spider_bp = Blueprint("spider", __name__, url_prefix="/spider")

@spider_bp.route('/update/')
def update_news():
    return jsonify({"message": "News update endpoint"})
