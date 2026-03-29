import os
from flask import request, jsonify
from main import db, app, tables
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_cors import cross_origin
from flask_restful import Resource
from error_handler import NotFoundError, DuplicateDataError, ForbiddenError, BadRequestError
from werkzeug.security import generate_password_hash, check_password_hash


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
UPLOAD_FOLDERS = {
    'manga_pics': os.path.join(os.path.dirname(__file__), 'static', 'manga_pics'),
    'images': os.path.join(os.path.dirname(__file__), 'static', 'images'),
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def require_admin():
    identity = get_jwt_identity()
    admin = tables.Admins.query.filter(tables.Admins.email == identity).first()
    if not admin:
        raise ForbiddenError()


def get_json_or_400():
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequestError("Request body must be valid JSON")
    return data


def require_fields(data, fields):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        raise BadRequestError(f"Missing required fields: {', '.join(missing)}")


class BookAPI(Resource):

    @cross_origin()
    @jwt_required()
    def get(self):
        q = tables.Books.query.filter().all()
        l = []
        l1 = []
        for i in q:
            q1 = tables.Chapters.query.filter(tables.Chapters.book_id == i.book_id).all()
            for j in q1:
                l1.append({"chapter_id": j.chapter_id, "volume_no": j.volume_no, "chapter_no": j.chapter_no, "chapter_name": j.chapter_name})
            l.append({"book_id": i.book_id, "book_name": i.book_name, "author_name": i.author_name, "book_description": i.book_description, "book_genres": i.book_genres, "book_price": i.book_price, "book_cover": i.book_cover, "chapters": l1})
            l1 = []
        return jsonify({"msg": "Query Results", "result": (l)}), 200

    @cross_origin()
    @jwt_required()
    def post(self):
        require_admin()
        post_data = get_json_or_400()
        require_fields(post_data, ['book_name', 'author_name', 'book_description', 'book_genres', 'book_price', 'book_cover'])
        q1 = tables.Books.query.filter(tables.Books.book_name == post_data['book_name']).all()
        if len(q1) != 0:
            raise DuplicateDataError(f"Book '{post_data['book_name']}' already exists")
        q = tables.Books(book_name=post_data.get('book_name'), author_name=post_data.get("author_name"), book_description=post_data.get("book_description"), book_genres=post_data.get('book_genres'), book_price=post_data.get('book_price'), book_cover=post_data.get('book_cover'))
        db.session.add(q)
        db.session.commit()
        return jsonify({"msg": "Uploaded Successfully"}), 201

    @cross_origin()
    @jwt_required()
    def put(self, book_id):
        require_admin()
        update_data = get_json_or_400()

        q = tables.Books.query.filter(tables.Books.book_id == book_id).first()
        if not q:
            raise NotFoundError(f"Book with id {book_id} not found")
        if update_data.get('book_name'):
            q1 = tables.Books.query.filter(tables.Books.book_name == update_data['book_name']).first()
            if q1 and q1.book_id != q.book_id:
                raise DuplicateDataError(f"Book name '{update_data['book_name']}' already taken")
        q.book_name = update_data.get('book_name') or q.book_name
        q.author_name = update_data.get('author_name') or q.author_name
        q.book_description = update_data.get('book_description') or q.book_description
        q.book_genres = update_data.get('book_genres') or q.book_genres
        q.book_price = update_data.get('book_price') or q.book_price
        q.book_cover = update_data.get('book_cover') or q.book_cover

        db.session.commit()
        return jsonify({"msg": "Updated Successfully"}), 200

    @cross_origin()
    @jwt_required()
    def delete(self, book_id):
        require_admin()
        q = tables.Books.query.filter(tables.Books.book_id == book_id).first()
        if not q:
            raise NotFoundError(f"Book with id {book_id} not found")
        q1 = tables.Chapters.query.filter(tables.Chapters.book_id == book_id).all()
        q2 = tables.Feedbacks.query.filter(tables.Feedbacks.book_id == book_id).all()
        q3 = tables.Watchlist.query.filter(tables.Watchlist.book_id == book_id).all()
        q4 = tables.Status.query.filter(tables.Status.book_id == book_id).all()
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
        return jsonify({"msg": "Deleted Successfully"}), 200

class ChapterAPI(Resource):
    @cross_origin()
    @jwt_required()
    def get(self):
        q = tables.Chapters.query.filter().order_by(tables.Chapters.chapter_no).all()
        l = []
        for i in q:
            l.append({"book_id": i.book_id, "chapter_no": i.chapter_no, "volume_no": i.volume_no, "chapter_title": i.chapter_name, "chapter_pages": i.chapter_pages})
        return jsonify({"msg": "Query Result", "result": (l)}), 200

    @cross_origin()
    @jwt_required()
    def post(self):
        require_admin()
        post_data = get_json_or_400()
        require_fields(post_data, ['volume_no', 'chapter_no', 'chapter_name', 'chapter_pages', 'book_id'])
        q1 = tables.Chapters.query.filter(tables.Chapters.volume_no == post_data["volume_no"], tables.Chapters.chapter_no == post_data["chapter_no"], tables.Chapters.book_id == post_data['book_id']).all()
        if len(q1) != 0:
            raise DuplicateDataError("This chapter already exists for the given book")
        q = tables.Chapters(volume_no=post_data.get('volume_no'), chapter_no=post_data.get('chapter_no'), chapter_name=post_data.get('chapter_name'), chapter_pages=post_data.get('chapter_pages'), book_id=post_data.get('book_id'))
        db.session.add(q)
        db.session.commit()
        return jsonify({"msg": "Uploaded Successfully"}), 201

    @cross_origin()
    @jwt_required()
    def put(self, chapter_id):
        require_admin()
        update_data = get_json_or_400()

        q = tables.Chapters.query.filter(tables.Chapters.chapter_id == chapter_id).first()
        if not q:
            raise NotFoundError(f"Chapter with id {chapter_id} not found")
        if update_data.get('volume_no') and update_data.get('chapter_no'):
            q1 = tables.Chapters.query.filter(tables.Chapters.volume_no == update_data.get('volume_no'), tables.Chapters.chapter_no == update_data.get('chapter_no')).first()
            if q1 and q1.chapter_id != q.chapter_id:
                raise DuplicateDataError("This volume/chapter combination already exists")
        q.volume_no = update_data.get('volume_no') or q.volume_no
        q.chapter_no = update_data.get('chapter_no') or q.chapter_no
        q.chapter_name = update_data.get('chapter_name') or q.chapter_name
        q.chapter_pages = update_data.get('chapter_pages') or q.chapter_pages

        db.session.commit()
        return jsonify({"msg": "Updated Successfully"}), 200

    @cross_origin()
    @jwt_required()
    def delete(self, chapter_id):
        require_admin()
        q = tables.Chapters.query.filter(tables.Chapters.chapter_id == chapter_id).first()
        if not q:
            raise NotFoundError(f"Chapter with id {chapter_id} not found")

        db.session.delete(q)
        db.session.commit()
        return jsonify({"msg": "Deleted Successfully"}), 200


class FeedbackAPI(Resource):

    @cross_origin()
    @jwt_required()
    def get(self):
        q1 = tables.Feedbacks.query.filter().all()
        l = []
        for i in q1:
            l.append({"book_id": i.book_id, "user_id": i.user_id, "feedback_id": i.feedback_id, "feedback_message": i.feedback_message, "feedback_score": i.feedback_score})
        return jsonify({"msg": "Query Results", 'result': (l)}), 200

    @cross_origin()
    @jwt_required()
    def post(self):
        post_data = get_json_or_400()
        require_fields(post_data, ['book_id', 'user_id', 'feedback_message', 'feedback_score'])
        q = tables.Feedbacks(book_id=post_data.get('book_id'), user_id=post_data.get("user_id"), feedback_message=post_data.get("feedback_message"), feedback_score=post_data.get('feedback_score'))
        db.session.add(q)
        db.session.commit()
        return jsonify({"msg": "Uploaded Successfully"}), 201

    @cross_origin()
    @jwt_required()
    def put(self, feedback_id):
        update_data = get_json_or_400()
        q = tables.Feedbacks.query.filter(tables.Feedbacks.feedback_id == feedback_id).first()
        if not q:
            raise NotFoundError(f"Feedback with id {feedback_id} not found")
        q.feedback_message = update_data.get('feedback_message') or q.feedback_message
        q.feedback_score = update_data.get('feedback_score') or q.feedback_score
        db.session.commit()
        return jsonify({"msg": "Updated Successfully"}), 200

    @cross_origin()
    @jwt_required()
    def delete(self, feedback_id):
        q = tables.Feedbacks.query.filter(tables.Feedbacks.feedback_id == feedback_id).first()
        if not q:
            raise NotFoundError(f"Feedback with id {feedback_id} not found")
        db.session.delete(q)
        db.session.commit()
        return jsonify({"msg": "Deleted Successfully"}), 200


class WatchlistAPI(Resource):

    @cross_origin()
    @jwt_required()
    def get(self):
        q1 = tables.Watchlist.query.filter().all()
        l = []
        for i in q1:
            l.append({"book_id": i.book_id, "user_id": i.user_id})
        return jsonify({"msg": "Query Results", 'result': (l)}), 200

    @cross_origin()
    @jwt_required()
    def post(self):
        post_data = get_json_or_400()
        require_fields(post_data, ['book_id', 'user_id'])
        q = tables.Watchlist(book_id=post_data.get('book_id'), user_id=post_data.get("user_id"))
        db.session.add(q)
        db.session.commit()
        return jsonify({"msg": "Uploaded Successfully"}), 201

    @cross_origin()
    @jwt_required()
    def delete(self, user_id, book_id):
        q = tables.Watchlist.query.filter(tables.Watchlist.user_id == user_id, tables.Watchlist.book_id == book_id).first()
        if not q:
            raise NotFoundError("Watchlist entry not found")
        db.session.delete(q)
        db.session.commit()
        return jsonify({"msg": "Deleted Successfully"}), 200

class UserRegisterAPI(Resource):
    @cross_origin()
    def post(self):
        post_data = get_json_or_400()
        require_fields(post_data, ['user_name', 'email', 'password'])
        q1 = tables.Users.query.filter(tables.Users.email == post_data["email"]).all()
        q2 = tables.Users.query.filter(tables.Users.user_name == post_data["user_name"]).all()
        if len(q1) != 0:
            raise DuplicateDataError("Email already registered")
        if len(q2) != 0:
            raise DuplicateDataError("Username already taken")
        q3 = tables.Users(user_name=post_data.get('user_name'), email=post_data.get('email'), password=generate_password_hash(post_data.get('password')))
        db.session.add(q3)
        db.session.commit()
        return jsonify({"msg": "Registered Successfully"}), 201

class UserLoginAPI(Resource):
    @cross_origin()
    def post(self):
        post_data = get_json_or_400()
        require_fields(post_data, ['email', 'password'])
        q = tables.Users.query.filter(tables.Users.email == post_data["email"]).first()
        if not q or not check_password_hash(q.password, post_data["password"]):
            raise NotFoundError("Invalid email or password")

        access_token = create_access_token(identity=post_data["email"])
        return jsonify({"msg": "valid user", "result": [q.user_id, access_token]}), 200

class AdminRegisterAPI(Resource):
    @cross_origin()
    @jwt_required()
    def post(self):
        require_admin()
        post_data = get_json_or_400()
        require_fields(post_data, ['admin_name', 'email', 'password'])
        q1 = tables.Admins.query.filter(tables.Admins.email == post_data["email"]).first()
        if q1:
            raise DuplicateDataError("Admin email already registered")
        q2 = tables.Admins.query.filter(tables.Admins.admin_name == post_data["admin_name"]).first()
        if q2:
            raise DuplicateDataError("Admin name already taken")
        admin = tables.Admins(admin_name=post_data.get('admin_name'), email=post_data.get('email'), password=generate_password_hash(post_data.get('password')))
        db.session.add(admin)
        db.session.commit()
        return jsonify({"msg": "Admin Registered Successfully"}), 201

class AdminLoginAPI(Resource):
    @cross_origin()
    def post(self):
        post_data = get_json_or_400()
        require_fields(post_data, ['email', 'password'])
        admin = tables.Admins.query.filter(tables.Admins.email == post_data["email"]).first()
        if not admin or not check_password_hash(admin.password, post_data["password"]):
            raise NotFoundError("Invalid admin credentials")

        access_token = create_access_token(identity=admin.email)
        return jsonify({"msg": "valid admin", "result": access_token}), 200

class UserAPI(Resource):
    @cross_origin()
    @jwt_required()
    def get(self):
        q = tables.Users.query.filter().all()
        l = []
        l1 = []
        l2 = []
        l3 = []
        for i in q:
            q1 = tables.Feedbacks.query.filter(tables.Feedbacks.user_id == i.user_id).all()
            q2 = tables.Status.query.filter(tables.Status.user_id == i.user_id, tables.Status.status_type == "accept").all()
            q3 = tables.Status.query.filter(tables.Status.user_id == i.user_id, tables.Status.status_type == "buy").all()
            for j in q1:
                l1.append({"feedback_score": j.feedback_score, "feedback_message": j.feedback_message, "book_id": j.book_id})
            for k in q3:
                l2.append({"book_id": k.book_id})
            for m in q2:
                l3.append({"expiry_date": m.expiry, "book_id": m.book_id})

            l.append({"user_id": i.user_id, "user_name": i.user_name, "email": i.email, "profile_banner": i.profile_banner, "profile_pic": i.profile_pic, "feedbacks": l1, "books_purchased": l2, "books_issued": l3})
            l1 = []
            l2 = []
            l3 = []
        return jsonify({"msg": "Query Results", "result": (l)}), 200

    @cross_origin()
    @jwt_required()
    def put(self, user_id):
        update_data = get_json_or_400()
        q = tables.Users.query.filter(tables.Users.user_id == user_id).first()
        if not q:
            raise NotFoundError(f"User with id {user_id} not found")
        if update_data.get("email"):
            q1 = tables.Users.query.filter(tables.Users.email == update_data["email"]).first()
            if q1 and q1.user_id != int(user_id):
                raise DuplicateDataError("Email already registered")
        if update_data.get("username"):
            q2 = tables.Users.query.filter(tables.Users.user_name == update_data["username"]).first()
            if q2 and q2.user_id != int(user_id):
                raise DuplicateDataError("Username already taken")
        q.user_name = update_data.get('username') or q.user_name
        q.email = update_data.get('email') or q.email
        if update_data.get('password'):
            q.password = generate_password_hash(update_data['password'])
        q.profile_pic = update_data.get('profile_pic') or q.profile_pic
        q.profile_banner = update_data.get('banner') or q.profile_banner
        db.session.commit()
        return jsonify({"msg": "Updated Successfully"}), 200

    @cross_origin()
    @jwt_required()
    def delete(self, user_id):
        q = tables.Users.query.filter(tables.Users.user_id == user_id).first()
        if not q:
            raise NotFoundError(f"User with id {user_id} not found")
        q1 = tables.Feedbacks.query.filter(tables.Feedbacks.user_id == user_id).all()
        q2 = tables.Watchlist.query.filter(tables.Watchlist.user_id == user_id).all()
        q3 = tables.Status.query.filter(tables.Status.user_id == user_id).all()
        for i in q3:
            db.session.delete(i)
        for i in q2:
            db.session.delete(i)
        for i in q1:
            db.session.delete(i)
        db.session.delete(q)
        db.session.commit()
        return jsonify({"msg": "Deleted Successfully"}), 200

class StatusAPI(Resource):
    @cross_origin()
    @jwt_required()
    def get(self):
        q = tables.Status.query.filter().all()
        l = []
        for i in q:
            q2 = tables.Books.query.filter(tables.Books.book_id == i.book_id).first()
            q1 = tables.Users.query.filter(tables.Users.user_id == i.user_id).first()
            if not q2 or not q1:
                continue
            l.append({"book_id": q2.book_id, "book_name": q2.book_name, "book_author": q2.author_name, "book_cover": q2.book_cover, "user_id": q1.user_id, "user_name": q1.user_name, "email": q1.email, "profile_pic": q1.profile_pic, "status_id": i.status_id, "expiry": i.expiry, "price": i.price, "status_type": i.status_type})
        return jsonify({"msg": "Query Results", "result": (l)}), 200

    @cross_origin()
    @jwt_required()
    def post(self, query):
        post_data = get_json_or_400()
        if query == "request":
            require_fields(post_data, ['user_id', 'book_id', 'expiry'])
            q = tables.Status(user_id=post_data["user_id"], book_id=post_data["book_id"], expiry=post_data["expiry"], price='', status_type="request")
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg": "Your request has been submitted"}), 201
        elif query == "buy":
            require_fields(post_data, ['user_id', 'book_id', 'price'])
            q = tables.Status(user_id=post_data["user_id"], book_id=post_data["book_id"], expiry="", price=post_data['price'], status_type="buy")
            db.session.add(q)
            db.session.commit()
            return jsonify({"msg": "Purchased Successfully"}), 201
        else:
            raise BadRequestError(f"Invalid query parameter: {query}")

    @cross_origin()
    @jwt_required()
    def put(self, query, user_id, book_id):
        if query == "accept":
            require_admin()
            q = tables.Status.query.filter(tables.Status.user_id == user_id, tables.Status.book_id == book_id, tables.Status.status_type == "request").first()
            if not q:
                raise NotFoundError("No pending request found for this user/book")
            q.status_type = "accept"
            db.session.commit()
            return jsonify({"msg": "Accepted"}), 200
        elif query == "expiry":
            update_data = get_json_or_400()
            require_fields(update_data, ['expiry'])
            q = tables.Status.query.filter(tables.Status.user_id == user_id, tables.Status.book_id == book_id, tables.Status.status_type == "accept").first()
            if not q:
                raise NotFoundError("No accepted status found for this user/book")
            q.expiry = update_data['expiry']
            db.session.commit()
            return jsonify({'msg': "Updated Successfully"}), 200
        else:
            raise BadRequestError(f"Invalid query parameter: {query}")

    @cross_origin()
    @jwt_required()
    def delete(self, query, user_id, book_id):
        if query == "reject":
            require_admin()
            q = tables.Status.query.filter(tables.Status.user_id == user_id, tables.Status.book_id == book_id, tables.Status.status_type == "request").first()
            if not q:
                raise NotFoundError("No pending request found for this user/book")
            db.session.delete(q)
            db.session.commit()
            return jsonify({"msg": "Rejected"}), 200
        elif query == "revoke":
            require_admin()
            q1 = tables.Status.query.filter(tables.Status.user_id == user_id, tables.Status.book_id == book_id, tables.Status.status_type == "accept").first()
            if not q1:
                raise NotFoundError("No accepted status found for this user/book")
            db.session.delete(q1)
            db.session.commit()
            return jsonify({"msg": "Revoked"}), 200
        elif query == "auto_revoke":
            q2 = tables.Status.query.filter(tables.Status.user_id == user_id, tables.Status.book_id == book_id, tables.Status.status_type == "accept").first()
            if not q2:
                raise NotFoundError("No accepted status found for this user/book")
            db.session.delete(q2)
            db.session.commit()
            return jsonify({"msg": "Revoked"}), 200
        else:
            raise BadRequestError(f"Invalid query parameter: {query}")


class UploadAPI(Resource):
    @cross_origin()
    @jwt_required()
    def post(self):
        folder = request.args.get('folder', 'manga_pics')
        if folder not in UPLOAD_FOLDERS:
            raise BadRequestError(f"Invalid folder: {folder}. Must be 'manga_pics' or 'images'")

        if 'file' not in request.files:
            raise BadRequestError("No file provided")

        files = request.files.getlist('file')
        filenames = []

        for f in files:
            if f.filename == '':
                continue
            if not allowed_file(f.filename):
                raise BadRequestError(f"File type not allowed: {f.filename}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDERS[folder], filename))
            filenames.append(filename)

        if not filenames:
            raise BadRequestError("No valid files uploaded")

        return jsonify({"msg": "Uploaded Successfully", "filenames": filenames}), 201
