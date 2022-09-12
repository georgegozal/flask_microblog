from flask import render_template,Blueprint
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

# app_view = Blueprint('app_view',__name__,template_folder="templates")

# # Invalid URL
# @app_view.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# # Internal Server Error
# @app_view.errorhandler(500)
# def page_not_found(e):
#     return render_template('500.html'), 500

# # @app_view.context_processor
# # def base():
# #     searchform = SearchForm()
# #     return dict(searchform=searchform)