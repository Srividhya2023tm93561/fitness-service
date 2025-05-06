from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb://mongo:27017")
db = client["fitness_db"]

# Utility function to convert ObjectId to string
def convert_objectid_to_str(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    return data

@app.route('/api/reports', methods=['GET'])
def get_report():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        # Fetch user data from fitness-user-service
        user_response = requests.get(f"http://fitness-user-service:5001/api/users/{user_id}")
        user_data = user_response.json()

        # Fetch meal data from fitness-meal-tracker-service
        meals_response = requests.get(f"http://fitness-meal-tracker-service:5002/api/meals/{user_id}")
        meals_data = meals_response.json()

        # Fetch workout data from fitness-workout-service
        workouts_response = requests.get(f"http://fitness-workout-service:5003/api/workouts/{user_id}")
        workouts_data = workouts_response.json()

        # Combine data into a report
        report = {
            "user": user_data,
            "meals": meals_data,
            "workouts": workouts_data
        }

        # Convert ObjectId to string in all nested data
        report = convert_objectid_to_str(report)

        return jsonify(report), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
