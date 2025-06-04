
import os
from pymongo import MongoClient
from datetime import datetime, timedelta

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["taxi_app"]
reports = db["reports"]

def save_report(location, status):
    report = {
        "location": location.lower(),
        "status": status,
        "timestamp": datetime.utcnow()
    }
    reports.insert_one(report)

def get_latest_status(location, lookback_minutes=60):
    location = location.lower()
    time_cutoff = datetime.utcnow() - timedelta(minutes=lookback_minutes)
    recent_reports = reports.find({
        "location": location,
        "timestamp": {"$gte": time_cutoff}
    }).sort("timestamp", -1)

    status_list = [r["status"] for r in recent_reports]
    unique_statuses = list(dict.fromkeys(status_list))  # Deduplicate in order

    if not unique_statuses:
        return "no recent updates."

    return " and ".join(unique_statuses)
