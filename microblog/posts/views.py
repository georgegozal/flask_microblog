from flask import Flask, flash,url_for, redirect,render_template,Blueprint, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

posts = Blueprint('posts',__name__,template_folder="templates/posts")
