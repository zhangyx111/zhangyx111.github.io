from flask import render_template
from .views import auth_bp

@auth_bp.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('errors/401.html'), 401
