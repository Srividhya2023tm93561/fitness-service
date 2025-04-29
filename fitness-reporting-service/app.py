from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/report", methods=["GET"])
def get_report():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = requests.get(f"http://fitness-user-service:5001/api/users/{user_id}").json()
    meals = requests.get(f"http://fitness-meal-tracker-service:5002/api/meals/{user_id}").json()
    workouts = requests.get(f"http://fitness-workout-service:5003/api/workouts/{user_id}").json()

    return jsonify({"user": user, "meals": meals, "workouts": workouts})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)