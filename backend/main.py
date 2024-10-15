import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from celery import Celery
from cache_config import create_cache
from datetime import timedelta 
from flask_jwt_extended import JWTManager

app = Flask(__name__)


app.config['SECRET_KEY']='secretkey'

#JWT Setup

app.config["JWT_SECRET_KEY"] = "wqfewfwefwefwefwefwf"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3.0)
jwt=JWTManager(app)


CORS(app,origins="*")



currdir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(currdir,"./database/mangaOasis.db")

db= SQLAlchemy()
db.init_app(app)

import tables

with app.app_context():
    db.create_all()

# Celery Setup

celery=Celery(app.import_name)
celery.conf.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2',
    timezone='Asia/Kolkata'
)
class CeleryTask(celery.Task):
    def __call__(self,*args,**kwargs):
        with app.app_context():
            print("Creating a new Task")
            return self.run(*args,**kwargs)

celery.Task=CeleryTask



#Cache Setup

cache=create_cache(app)
app.app_context().push()



from api import UserAPI,UserLoginAPI,UserRegisterAPI,AdminLoginAPI,BookAPI,FeedbackAPI,WatchlistAPI,StatusAPI,ChapterAPI

api=Api(app)
api.add_resource(UserAPI,"/user","/user/<user_id>")  
api.add_resource(UserLoginAPI,"/login_user") 
api.add_resource(UserRegisterAPI,"/register_user") 
api.add_resource(AdminLoginAPI,"/login_admin") 
api.add_resource(BookAPI,"/book","/book/<book_id>") 
api.add_resource(FeedbackAPI,"/feedback","/feedback/<feedback_id>") 
api.add_resource(WatchlistAPI,"/watchlist","/watchlist/<user_id>/<book_id>") 
api.add_resource(StatusAPI,"/get_status","/status/<query>","/status/<query>/<user_id>/<book_id>") 
api.add_resource(ChapterAPI,"/chapter","/chapter/<chapter_id>") 