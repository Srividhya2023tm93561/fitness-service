from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client["fitness"]
users = db["users"]

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    data["user_id"] = str(data["user_id"])
    users.insert_one(data)
    return jsonify({"message": "User created"}), 201

@app.route("/api/users", methods=["GET"])
def get_users():
    user_list = list(users.find({}, {"_id": 0}))
    return jsonify(user_list)

@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = users.find_one({"user_id": user_id}, {"_id": 0})
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)