from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client["fitness"]
meals = db["meals"]

@app.route("/api/meals", methods=["POST"])
def create_meal():
    data = request.json
    data["user_id"] = str(data["user_id"])
    meals.insert_one(data)
    return jsonify({"message": "Meal added"}), 201

@app.route("/api/meals", methods=["GET"])
def get_meals():
    meal_list = list(meals.find({}, {"_id": 0}))
    return jsonify(meal_list)

@app.route("/api/meals/<user_id>", methods=["GET"])
def get_meals_by_user(user_id):
    meal_list = list(meals.find({"user_id": user_id}, {"_id": 0}))
    return jsonify(meal_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)