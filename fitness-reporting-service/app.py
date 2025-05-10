from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb://mongo:27017")
db = client["fitness"]
reports = db["reports"]

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
        user_response.raise_for_status()
        user_data = user_response.json()

        # Fetch meal data from fitness-meal-tracker-service
        meals_response = requests.get(f"http://fitness-meal-tracker-service:5002/api/meals/{user_id}")
        meals_response.raise_for_status()
        meals_data = meals_response.json()

        # Fetch workout data from fitness-workout-service
        workouts_response = requests.get(f"http://fitness-workout-service:5003/api/workouts/{user_id}")
        workouts_response.raise_for_status()
        workouts_data = workouts_response.json()

        # Combine data into a report
        report = {
            "user_id": user_id,
            "user": user_data,
            "meals": meals_data,
            "workouts": workouts_data
        }

        # Insert report into MongoDB after converting ObjectIds
        report_to_store = convert_objectid_to_str(report)
        inserted_id = reports.insert_one(report_to_store).inserted_id

        # Add the inserted Mongo ID to the response
        report_to_store["_id"] = str(inserted_id)

        return jsonify(report_to_store), 200

    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Service call failed: {req_err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
