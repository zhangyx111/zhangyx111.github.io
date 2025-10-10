from flask import jsonify
from . import api
from ..services.spider import NewsCrawler, DailyFAISSHelper

@api.route('/update/')
def update_news():
    return jsonify({"message": "News update endpoint"})
