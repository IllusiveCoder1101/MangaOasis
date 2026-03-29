import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
from error_handler import register_error_handlers

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'

# JWT Setup
app.config["JWT_SECRET_KEY"] = "wqfewfwefwefwefwefwf"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3.0)
jwt = JWTManager(app)

CORS(app, origins="*")

currdir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(currdir, "./database/mangaOasis.db")

db = SQLAlchemy()
db.init_app(app)

register_error_handlers(app, jwt, db)

import tables

with app.app_context():
    db.create_all()

from api import UserAPI, UserLoginAPI, UserRegisterAPI, AdminLoginAPI, AdminRegisterAPI, BookAPI, FeedbackAPI, WatchlistAPI, StatusAPI, ChapterAPI, UploadAPI

api = Api(app)
api.add_resource(UserAPI, "/user", "/user/<user_id>")
api.add_resource(UserLoginAPI, "/login_user")
api.add_resource(UserRegisterAPI, "/register_user")
api.add_resource(AdminLoginAPI, "/login_admin")
api.add_resource(AdminRegisterAPI, "/register_admin")
api.add_resource(BookAPI, "/book", "/book/<book_id>")
api.add_resource(FeedbackAPI, "/feedback", "/feedback/<feedback_id>")
api.add_resource(WatchlistAPI, "/watchlist", "/watchlist/<user_id>/<book_id>")
api.add_resource(StatusAPI, "/get_status", "/status/<query>", "/status/<query>/<user_id>/<book_id>")
api.add_resource(ChapterAPI, "/chapter", "/chapter/<chapter_id>")
api.add_resource(UploadAPI, "/upload")
