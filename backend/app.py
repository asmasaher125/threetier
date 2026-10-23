from flask import Flask, jsonify
from pymongo import MongoClient, ReturnDocument
import os

app = Flask(__name__)

def get_db():
    client = MongoClient(os.getenv("MONGO_HOST", "db_c"), 27017,
                         serverSelectionTimeoutMS=3000)
    return client.appdb

@app.route("/api/health")
def health():
    return jsonify(status="ok", version=os.getenv("APP_VERSION", "1"))

@app.route("/api/visit")
def visit():
    doc = get_db().counter.find_one_and_update(
        {"_id": "visits"}, {"$inc": {"count": 1}},
        upsert=True, return_document=ReturnDocument.AFTER)
    return jsonify(visits=doc["count"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
