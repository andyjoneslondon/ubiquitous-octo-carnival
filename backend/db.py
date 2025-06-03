from pymongo import MongoClient
import os
import datetime

# Connect to MongoDB using the URI from environment variables
client = MongoClient(os.getenv("MONGO_URI"))

# Access the database and collection
db = client["taxi_app"]
reports = db["reports"]

def save_report(location, status):
    reports.insert_one({
        "location": location,
        "status": status,
        "timestamp": datetime.datetime.utcnow()
    })

def get_latest_status(location):
    doc = reports.find_one(
        {"location": location},
        sort=[("timestamp", -1)]
    )
    return doc["status"] if doc else "No recent reports for this location."