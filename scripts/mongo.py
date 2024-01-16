import json

from datetime import datetime

from src.mongo import MongoConnector

HOST = "mongodb://172.17.0.2"
PORT = 27017
DATABASE = "ABC"

def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

print("Connecting to MongoDB...")
mongo = MongoConnector(HOST, PORT, DATABASE)
    
print("Loading schemas...")
users_schema = read_json("db/schemas/user.json")
features_schema = read_json("db/schemas/feature.json")
activities_schema = read_json("db/schemas/activity.json")

print("Create the collections in Mogo DB")
if not mongo.collection_exists("users"):
    mongo.create_collection("users", validator=users_schema)
if not mongo.collection_exists("features"):
    mongo.create_collection("features", validator=features_schema)
if not mongo.collection_exists("activities"):
    mongo.create_collection("activities", validator=activities_schema)
    
print("Loading mock data...")
users = read_json("db/data/users.jsonl")
features = read_json("db/data/features.jsonl")

print("Inserting mock data...")
for user in users:
    if mongo._db["users"].find_one({"userId": user["userId"]}) is None:
        user["registrationDate"] = datetime.strptime(user["registrationDate"], "%Y-%m-%dT%H:%M:%SZ")
        mongo.add_document("users", user)
        
for feature in features:
    if mongo._db["features"].find_one({"featureId": feature["featureId"]}) is None:
        if feature.get("launchDate"):
            feature["launchDate"] = datetime.strptime(feature["launchDate"], "%Y-%m-%dT%H:%M:%SZ")
        mongo.add_document("features", feature)

print(mongo._db["users"].find_one({"userId": "1"}))
# print(mongo.get_db())