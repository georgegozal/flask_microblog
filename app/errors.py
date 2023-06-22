from flask import render_template, Blueprint


errors = Blueprint('errors', __name__)


# Invalid URL
@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
