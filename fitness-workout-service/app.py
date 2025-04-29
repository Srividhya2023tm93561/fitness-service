from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client["fitness"]
workouts = db["workouts"]

@app.route("/api/workouts", methods=["POST"])
def create_workout():
    data = request.json
    data["user_id"] = str(data["user_id"])
    workouts.insert_one(data)
    return jsonify({"message": "Workout added"}), 201

@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    workout_list = list(workouts.find({}, {"_id": 0}))
    return jsonify(workout_list)

@app.route("/api/workouts/<user_id>", methods=["GET"])
def get_workouts_by_user(user_id):
    workout_list = list(workouts.find({"user_id": user_id}, {"_id": 0}))
    return jsonify(workout_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)