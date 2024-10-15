from flask import request,jsonify
from main import db,app,tables,cache
import access_data
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from flask_cors import cross_origin
from flask_restful import Resource
from error_handler import NotFoundError, DuplicateDataError
from time import perf_counter_ns

class BookAPI(Resource):
    
    @cross_origin()
    @jwt_required()
    def get(self):
        if get_jwt_identity():
            start=perf_counter_ns()
            q=tables.Books.query.filter().all()
            stop=perf_counter_ns()
            print("Time",stop-start)
            l=[]
            l1=[]
            for i in q:
                q1=tables.Chapters.query.filter(tables.Chapters.book_id == i.book_id).all()
                for j in q1:
                    l1.append({"chapter_id":j.chapter_id,"volume_no":j.volume_no,"chapter_no":j.chapter_no,"chapter_name":j.chapter_name})
                l.append({"book_id":i.book_id,"book_name":i.book_name,"author_name":i.author_name,"book_description":i.book_description,"book_genres":i.book_genres,"book_price":i.book_price,"book_cover":i.book_cover,"chapters":l1})
                l1=[]
            return jsonify({"msg":"Query Results","result":(l)}),201  
    
    @cross_origin()
    @jwt_required()     
    def post(self):
        if get_jwt_identity()=="admin2004@gmail.com":
            post_data=request.get_json()
            q1=tables.Books.query.filter(tables.Books.book_name == post_data['book_name']).all()
            if len(q1)!=0:
                raise DuplicateDataError(status_code=402)        
            q=tables.Books(book_name=post_data.get('book_name'),author_name=post_data.get("author_name"),book_description=post_data.get("book_description"),book_genres=post_data.get('book_genres'),book_price=post_data.get('book_price'),book_cover=post_data.get('book_cover'))
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg":"Uploaded Succesfully"}),201 
        
    @cross_origin()
    @jwt_required()    
    def put(self,book_id):
        if get_jwt_identity()=="admin2004@gmail.com":
            update_data=request.get_json()
            
            q=tables.Books.query.filter(tables.Books.book_id==book_id).first()
            if(not q):
                raise NotFoundError(status_code=404)
            q1=tables.Books.query.filter(tables.Books.book_name == update_data['book_name']).all()
            if(q1):
                if (q1.book_id!=q.book_id):
                    raise DuplicateDataError(status_code=402)
            q.book_name=update_data.get('book_name')  or q.book_name
            q.author_name=update_data.get('author_name')  or q.author_name
            q.book_description=update_data.get('book_description')  or q.book_description
            q.book_genres=update_data.get('book_genres')  or q.book_genres
            q.book_price=update_data.get('book_price')  or q.book_price
            q.book_cover=update_data.get('book_cover')  or q.book_cover       
            
            db.session.commit()
            return jsonify({"msg":"Updated Successfully"}),201
        
    @cross_origin()
    @jwt_required()
    def delete(self,book_id):
        if get_jwt_identity()=="admin2004@gmail.com":
            q=tables.Books.query.filter(tables.Books.book_id == book_id).first()
            q1=tables.Chapters.query.filter(tables.Chapters.book_id == book_id).all()
            q2=tables.Feedbacks.query.filter(tables.Feedbacks.book_id == book_id).all()
            q3=tables.Watchlist.query.filter(tables.Watchlist.book_id == book_id).all()
            q4=tables.Status.query.filter(tables.Status.book_id == book_id).all()
            if(not q):
               raise NotFoundError(status_code=404)
            for i in q4:
                db.session.delete(i)
            for i in q3:
                db.session.delete(i)
            for i in q2:
                db.session.delete(i)
            for i in q1:
                db.session.delete(i)
            db.session.delete(q)
            db.session.commit()
            return jsonify({"msg":"Deleted Successfully"}),201

class ChapterAPI(Resource):
    @cross_origin()
    @jwt_required()
    def get(self):
        if get_jwt_identity():
            q=tables.Chapters.query.filter().order_by(tables.Chapters.chapter_no).all()
            l=[]
            for i in q:
                l.append({"book_id":i.book_id,"chapter_no":i.chapter_no,"volume_no":i.volume_no,"chapter_title":i.chapter_name,"chapter_pages":i.chapter_pages})
            return jsonify({"msg":"Query Result","result":(l)}),201
        
    @cross_origin()
    @jwt_required()
    def post(self):
        if get_jwt_identity() == "admin2004@gmail.com":
            post_data=request.get_json()
            q1=tables.Chapters.query.filter(tables.Chapters.volume_no==post_data["volume_no"], tables.Chapters.chapter_no == post_data["chapter_no"],tables.Chapters.book_id == post_data['book_id']).all()
            if len(q1)!=0:
                raise DuplicateDataError(status_code=402)
            q=tables.Chapters(volume_no=post_data.get('volume_no'),chapter_no=post_data.get('chapter_no'),chapter_name=post_data.get('chapter_name'),chapter_pages=post_data.get('chapter_pages'),book_id=post_data.get('book_id'))
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg":"Uploaded Successfully"}),201
        
    @cross_origin()
    @jwt_required()
    def put(self,chapter_id):
        if get_jwt_identity()=="admin2004@gmail.com":
            update_data=request.get_json()
            
            q=tables.Chapters.query.filter(tables.Chapters.chapter_id==chapter_id).first()

            if(not q):
               raise NotFoundError(status_code=404)
            q1=tables.Chapters.query.filter(tables.Chapters.volume_no==update_data.get('volume_no') ,tables.Chapters.chapter_no==update_data.get('chapter_no')).first()
            if(q1):
                if(q1.chapter_id!=q.chapter_id):
                    raise DuplicateDataError(status_code=402)
            q.volume_no=update_data.get('volume_no')  or q.volume_no
            q.chapter_no=update_data.get('chapter_no')  or q.chapter_no
            q.chapter_name=update_data.get('chapter_name')  or q.chapter_name
            q.chapter_pages=update_data.get('chapter_pages')  or q.chapter_pages       
            
            db.session.commit()
            return jsonify({"msg":"Updated Successfully"}),201
        
    @cross_origin()
    @jwt_required()
    def delete(self,chapter_id):
        if get_jwt_identity()=="admin2004@gmail.com":
            q=tables.Chapters.query.filter(tables.Chapters.chapter_id == chapter_id).first()
            if(not q):
                raise NotFoundError(status_code=404)
            
            db.session.delete(q)
            db.session.commit()
            return jsonify({"msg":"Deleted Successfully"}),201
    
    
class FeedbackAPI(Resource):

    @cross_origin()
    @jwt_required()
    def get(self):
        if get_jwt_identity():
            q1=tables.Feedbacks.query.filter().all()
            l=[]
            for i in q1:
                l.append({"book_id":i.book_id,"user_id":i.user_id,"feedback_id":i.feedback_id,"feedback_message":i.feedback_message,"feedback_score":i.feedback_score})
            return jsonify({"msg":"Query Results",'result':(l)}) ,201
        
    @cross_origin()
    @jwt_required()
    def post(self):
        if  get_jwt_identity():
            post_data=request.get_json()
            q=tables.Feedbacks(book_id=post_data.get('book_id'),user_id=post_data.get("user_id"),feedback_message=post_data.get("feedback_message"),feedback_score=post_data.get('feedback_score'))
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg":"Uploaded Successfully"}),201
        
    @cross_origin()
    @jwt_required()
    def put(self,feedback_id):
        if get_jwt_identity():
            update_data=request.get_json()
            q=tables.Feedbacks.query.filter(tables.Feedbacks.feedback_id==feedback_id).first()
            if (not q):
                raise NotFoundError(status_code=404)  
            q.feedback_message=update_data.get('feedback_message')  or q.feedback_message
            q.feedback_score=update_data.get('feedback_score')  or q.feedback_score
            db.session.commit()
            return jsonify({"msg":"Updated Successfully"}),201

    @cross_origin()
    @jwt_required()
    def delete(self,feedback_id):
        if get_jwt_identity():
            q=tables.Feedbacks.query.filter(tables.Feedbacks.feedback_id == feedback_id).first()
            if(not q):
                raise NotFoundError(status_code=404)
            db.session.delete(q)
            db.session.commit()
            return jsonify({"msg":"deleted Succesfully"}),201


class WatchlistAPI(Resource):

    @cross_origin()
    @jwt_required()
    def get(self):
        if get_jwt_identity():
            q1=tables.Watchlist.query.filter().all()
            l=[]
            for i in q1:
                l.append({"book_id":i.book_id,"user_id":i.user_id})
            return jsonify({"msg":"Query Results",'result':(l)}),201
    @cross_origin()
    @jwt_required()
    def post(self):
        if get_jwt_identity():
            post_data=request.get_json()
            q=tables.Watchlist(book_id=post_data.get('book_id'),user_id=post_data.get("user_id"))
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg":"Uploaded Successfully"}),201
    @cross_origin()
    @jwt_required()
    def delete(self,user_id,book_id):
        if get_jwt_identity():
            q=tables.Watchlist.query.filter(tables.Watchlist.user_id==user_id,tables.Watchlist.book_id == book_id).first()
            if(not q):
                raise NotFoundError(status_code=404)
            db.session.delete(q)
            db.session.commit()
            return jsonify({"msg":"deleted successfully"}),201

class UserRegisterAPI(Resource):
    @cross_origin()
    def post(self):
        post_data=request.get_json()
        q1=tables.Users.query.filter(tables.Users.email==post_data["email"]).all()
        q2=tables.Users.query.filter(tables.Users.user_name==post_data["user_name"]).all()
        if len(q1)!=0 and len(q2)!=0:
            raise DuplicateDataError(status_code=402)
        q3=tables.Users(user_name=post_data.get('user_name'),email=post_data.get('email'),password=post_data.get('password'))
        db.session.add(q3)
        db.session.commit()
        return jsonify({"msg":"Registered Succesfully"}),201

class UserLoginAPI(Resource):
    @cross_origin()
    def post(self):
        post_data=request.get_json()
        q=tables.Users.query.filter(tables.Users.email == post_data["email"],tables.Users.password == post_data["password"]).first()
        if(not q):
            raise NotFoundError(status_code=404)
        
        access_token=create_access_token(identity=post_data["email"])
        return jsonify({"msg":"valid user","result":[q.user_id,access_token]}), 201

class AdminLoginAPI(Resource):
    @cross_origin()
    def post(self):
        post_data=request.get_json()
        if(post_data["email"]!="admin2004@gmail.com" and post_data["password"]!="admin2004"):
            raise NotFoundError(status_code=404)
        
        access_token=create_access_token(identity="admin2004@gmail.com")
        res=jsonify({"msg":"valid admin","result":access_token})
        return res , 201

class UserAPI(Resource):
    @cross_origin()
    @jwt_required()
    def get(self):
        if get_jwt_identity():
            start=perf_counter_ns()
            q=tables.Users.query.filter().all()
            stop=perf_counter_ns()
            print("time",stop-start)
            l=[]
            l1=[]
            l2=[]
            l3=[]
            for i in q:
                q1=tables.Feedbacks.query.filter(tables.Feedbacks.user_id == i.user_id).all()
                q2=tables.Status.query.filter(tables.Status.user_id == i.user_id,tables.Status.status_type=="accept").all()
                q3=tables.Status.query.filter(tables.Status.user_id == i.user_id,tables.Status.status_type=="buy").all()
                for j in q1:
                    l1.append({"feedback_score":j.feedback_score,"feedback_message":j.feedback_message,"book_id":j.book_id})
                for k in q3:
                    l2.append({"book_id":k.book_id})
                for m in q2:
                    l3.append({"expiry_date":m.expiry,"book_id":m.book_id})
                
                l.append({"user_id":i.user_id,"user_name":i.user_name,"email":i.email,"password":i.password,"profile_banner":i.profile_banner,"profile_pic":i.profile_pic,"feedbacks":l1,"books_purchased":l2,"books_issued":l3})
                l1=[]
                l2=[]
                l3=[]
            return jsonify({"msg":"Query Results","result":(l)}),201
        
    @cross_origin()
    @jwt_required()
    def put(self,user_id):
        if get_jwt_identity():
            update_data=request.get_json()
            q1=tables.Users.query.filter(tables.Users.email==update_data["email"]).all()
            q2=tables.Users.query.filter(tables.Users.user_name==update_data["username"]).all()
            if len(q1)!=0 and len(q2)!=0:
                raise DuplicateDataError(status_code=402)
            q=tables.Users.query.filter(tables.Users.user_id==user_id).first()
            if (not q):
                raise NotFoundError(status_code=404)
            q.user_name=update_data.get('username')  or q.user_name
            q.email=update_data.get('email')  or q.email
            q.password=update_data.get('password')  or q.password
            q.profile_pic=update_data.get('profile_pic')  or q.profile_pic       
            q.profile_banner=update_data.get('banner') or q.profile_banner
            db.session.commit()
            return jsonify({"msg":"Updated Succesufully"}),201
    
    @cross_origin()
    @jwt_required()
    def delete(self,user_id):
        if get_jwt_identity():
            q=tables.Users.query.filter(tables.Users.user_id == user_id).first()
            q1=tables.Feedbacks.query.filter(tables.Feedbacks.user_id == user_id).all()
            q2=tables.Watchlist.query.filter(tables.Watchlist.user_id == user_id).all()
            q3=tables.Status.query.filter(tables.Status.user_id == user_id).all()
            if(not q):
                raise NotFoundError(status_code=404)
            for i in q3:
                db.session.delete(i)
            for i in q2:
                db.session.delete(i)
            for i in q1:
                db.session.delete(i)
            db.session.delete(q)
            db.session.commit()
            return jsonify({"msg":"Deleted Succesufully"}),201

class StatusAPI(Resource):
    @cross_origin()
    @jwt_required()
    def get(self):
        if get_jwt_identity():
            q=tables.Status.query.filter().all()
            l=[]
            for i in q:
                q2=tables.Books.query.filter(tables.Books.book_id == i.book_id).first()
                q1=tables.Users.query.filter(tables.Users.user_id==i.user_id).first()
                l.append({"book_id":q2.book_id,"book_name":q2.book_name,"book_author":q2.author_name,"book_cover":q2.book_cover,"user_id":q1.user_id,"user_name":q1.user_name,"email":q1.email,"profile_pic":q1.profile_pic,"status_id":i.status_id,"expiry":i.expiry,"price":i.price,"status_type":i.status_type})
            return jsonify({"msg":"Query Results","result":(l)}),201
        
    @cross_origin()
    @jwt_required()
    def post(self,query):
        if get_jwt_identity() and query=="request":
            post_data=request.get_json()
            q=tables.Status(user_id=post_data["user_id"],book_id=post_data["book_id"],expiry=post_data["expiry"],price='',status_type="request")
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg":"your request has been given"}),201
        elif get_jwt_identity() and query=="buy":
            post_data=request.get_json()
            q=tables.Status(user_id = post_data["user_id"],book_id = post_data["book_id"],expiry="",price=post_data['price'],status_type="buy")
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg":"Purchased Succesfully"}) ,201

    @cross_origin()
    @jwt_required()
    def put(self,query,user_id,book_id):
        if get_jwt_identity()=="admin2004@gmail.com" and query=="accept":
            q=tables.Status.query.filter(tables.Status.user_id == user_id,tables.Status.book_id==book_id,tables.Status.status_type=="request").first()
            if(not q):
                raise NotFoundError(status_code=404)
            q.status_type = "accept"
            db.session.commit()
            return jsonify({"msg":"Accepted"}) ,201
        elif query=="expiry" and get_jwt_identity():
            update_data=request.get_json()
            q=tables.Status.query.filter(tables.Status.user_id==user_id,tables.Status.book_id==book_id,tables.Status.status_type=="accept").first()
            if(not q):
                raise NotFoundError(status_code=404)
            q.expiry=update_data['expiry']
            db.session.commit()
            return jsonify({'msg':"Updated Succesufully"}),201
        
    @cross_origin()
    @jwt_required()
    def delete(self,query,user_id,book_id):
        if get_jwt_identity()=="admin2004@gmail.com" and query=="reject":
            q=tables.Status.query.filter(tables.Status.user_id==user_id,tables.Status.book_id == book_id,tables.Status.status_type == "request").first()
            if not q:
                raise NotFoundError(status_code=404)
            db.session.delete(q)
            db.session.commit()
            return jsonify({"msg":"Rejected"}) ,201
        elif get_jwt_identity()=="admin2004@gmail.com" and query=="revoke":  
            q1=tables.Status.query.filter(tables.Status.user_id==user_id,tables.Status.book_id == book_id,tables.Status.status_type == "accept").first()
            if not q1:
                raise NotFoundError(status_code=404)
            db.session.delete(q1)
            db.session.commit()
            return jsonify({"msg":"Revoked"}) ,201
        elif get_jwt_identity() and query=="auto_revoke":
            q2=tables.Status.query.filter(tables.Status.user_id==user_id,tables.Status.book_id == book_id,tables.Status.status_type == "accept").first()
            if not q2:
                raise NotFoundError(status_code=404)
            db.session.delete(q2)
            db.session.commit()
            return jsonify({"msg":"Revoked"}) ,201