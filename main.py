from app.create_app import create_app
from pymongo.errors import DuplicateKeyError
from flask import jsonify
from fastapi import HTTPException

app = create_app()
from app.api.routers.tests import test_bp
from app.api.routers.users import auth_bp
from app.api.routers.posts import post_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(test_bp, url_prefix="/tests")
app.register_blueprint(post_bp, url_prefix="/posts")


@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def resource_not_found(e):
    """
    An error-handler to ensure that 400 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 400


@app.errorhandler(405)
def resource_not_found(e):
    """
    An error-handler to ensure that 405 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 405


@app.errorhandler(DuplicateKeyError)
def resource_not_found(e):
    """
    An error-handler to ensure that MongoDB duplicate key errors are returned as JSON.
    """
    app.logger.error(e)
    return jsonify(detail=f"Duplicate key error."), 400


@app.errorhandler(HTTPException)
def resource_not_found(e: HTTPException):
    """
    An error-handler to ensure HTTPException are returned as JSON.
    """
    app.logger.error(e.detail)
    return jsonify(detail=e.detail), e.status_code


@app.errorhandler(Exception)
def resource_not_found(e):
    """
    An error-handler to ensure Exceptions are returned as JSON.
    """
    app.logger.error(e)
    return jsonify(detail=f"Internal Server Error"), 500


if __name__ == "__main__":
    app.run(debug=True)
