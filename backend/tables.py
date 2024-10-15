from main import db
#https://dbdiagram.io/d/66b86b918b4bb5230ec96631

class Users(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name=db.Column(db.String,nullable=False,unique=True)
    email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    profile_pic=db.Column(db.String,nullable=False,default="profile_pic.jpg")
    profile_banner=db.Column(db.String,nullable=False,default="banner1.jpg")

class Books(db.Model):
    __tablename__="book"
    book_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    book_name=db.Column(db.String,nullable=False,unique=True)
    author_name=db.Column(db.String,nullable=False)
    book_description=db.Column(db.String,nullable=False)
    book_genres=db.Column(db.String,nullable=False)
    book_price=db.Column(db.Integer,nullable=False)
    book_cover=db.Column(db.String,nullable=False) 

class Chapters(db.Model):
    __tablename__="chapter"
    chapter_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    volume_no=db.Column(db.Integer,nullable=False)
    chapter_no=db.Column(db.Integer,nullable=False)
    chapter_name=db.Column(db.String,nullable=False,unique=True)
    chapter_pages=db.Column(db.String,nullable=False)
    book_id=db.Column(db.Integer,db.ForeignKey("book.book_id"),nullable=False)

class Watchlist(db.Model):
    __tablename__="watchlist"
    watchlist_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    book_id=db.Column(db.Integer,db.ForeignKey("book.book_id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)

class Feedbacks(db.Model):
    __tablename__='feedback'
    feedback_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    book_id=db.Column(db.Integer,db.ForeignKey("book.book_id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    feedback_message=db.Column(db.String,nullable=False)
    feedback_score=db.Column(db.Integer,nullable=False)
    
class Status(db.Model):
    __tablename__="status"
    status_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    book_id=db.Column(db.Integer,db.ForeignKey("book.book_id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    expiry=db.Column(db.String,nullable=True)
    status_type=db.Column(db.String,nullable=False)
    price=db.Column(db.Integer,nullable=True)