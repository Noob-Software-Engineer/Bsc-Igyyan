from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

app = Flask(__name__)

# Configure JWT settings
app.config[
    "JWT_SECRET_KEY"
] = "your-secret-key"  # Change this to a strong, random secret key
jwt = JWTManager(app)
# Sample user data (replace with your user model)
users = [
    {"id": 1, "username": "user1", "password": "password1"},
    {"id": 2, "username": "user2", "password": "password2"},
]


# Registration route
@app.route("/register", methods=["POST"])
def register():
    # Get user data from the request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Create a new user (you can add user to a database here)
    user = {"id": len(users) + 1, "username": username, "password": password}
    users.append(user)

    return jsonify({"message": "User registered successfully"})


# Login route
@app.route("/login", methods=["POST"])
def login():
    # Get user data from the request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Find user by username (you can use a database query here)
    user = next((user for user in users if user["username"] == username), None)

    if user and user["password"] == password:
        # Create a JWT token
        access_token = create_access_token(identity=user)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid username or password"}), 401


# Protected route (requires authentication)
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    # Fetch user data from your database based on current_user_id
    # Return user information as needed
    return jsonify({"user": current_user})


if __name__ == "__main__":
    app.run(debug=True)
