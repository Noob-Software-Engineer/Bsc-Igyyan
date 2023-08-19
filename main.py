from app.create_app import app
from pymongo.errors import DuplicateKeyError
from flask import jsonify
from app.api.routers.users import auth_bp

app.register_blueprint(auth_bp, url_prefix="/auth")


@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404


@app.errorhandler(DuplicateKeyError)
def resource_not_found(e):
    """
    An error-handler to ensure that MongoDB duplicate key errors are returned as JSON.
    """
    return jsonify(error=f"Duplicate key error."), 400


if __name__ == "__main__":
    app.run(debug=True)
