from flask import jsonify
from werkzeug.exceptions import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, message="Data not found"):
        super().__init__(description=message)
        self.response = jsonify({"msg": message})
        self.response.status_code = 404


class DuplicateDataError(HTTPException):
    def __init__(self, message="Duplicate Data"):
        super().__init__(description=message)
        self.response = jsonify({"msg": message})
        self.response.status_code = 409


class ForbiddenError(HTTPException):
    def __init__(self, message="Admin access required"):
        super().__init__(description=message)
        self.response = jsonify({"msg": message})
        self.response.status_code = 403


class BadRequestError(HTTPException):
    def __init__(self, message="Bad request"):
        super().__init__(description=message)
        self.response = jsonify({"msg": message})
        self.response.status_code = 400


def register_error_handlers(app, jwt, db):

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"msg": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"msg": "Method not allowed"}), 405

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        if isinstance(e, HTTPException):
            raise e
        db.session.rollback()
        app.logger.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify({"msg": "Internal server error"}), 500

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token(error_string):
        return jsonify({"msg": "Invalid token"}), 401

    @jwt.unauthorized_loader
    def missing_token(error_string):
        return jsonify({"msg": "Missing authorization token"}), 401
