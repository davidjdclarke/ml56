# Design and Implementation of a RESTful API for Session Tracking

## MongoDB Schema
The MongoDB has three collections under the ABC database:
1. users: This collection stores the userId and the associated user name.
2. features: This collection stores the featureId and the associated feature name.
3. activity: This collection stores the userId, featureId, and the start and end times of the session.

The schemas follow as such:

### users
```json
{
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "userId",
            "email"
        ],
        "properties": {
            "userId": {
                "bsonType": "string"
            },
            "name": {
                "bsonType": "string"
            },
            "email": {
                "bsonType": "string"
            },
            "registrationDate": {
                "bsonType": "date"
            }
        }
    }
}
```

### Features
```json
{
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "featureId",
            "name"
        ],
        "properties": {
            "featureId": {
                "bsonType": "string"
            },
            "name": {
                "bsonType": "string"
            },
            "description": {
                "bsonType": "string"
            },
            "launchDate": {
                "bsonType": "date"
            }
        }
    }
}
```

### Activity
```json
{
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "userId",
            "featureId",
            "timestamp",
            "activityType"
        ],
        "properties": {
            "userId": {
                "bsonType": "string"
            },
            "featureId": {
                "bsonType": "string"
            },
            "timestamp": {
                "bsonType": "date"
            },
            "activityType": {
                "bsonType": "string"
            },
            "additionalNotes": {
                "bsonType": "string"
            }
        }
    }
}
```

# Getting Started

## Configure Python environment
Configure and activate the Python virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate

pip install -r requirements-test.txt
```

## Configuring the MongoDB
Start the MongoDB docker container

```bash
cd db/
./run.sh
```

Then execute the following commands to exec into the running docker and create the ABC database:

```bash
docker exec -it mongo mongosh
test > use ABC
```

Next, run the script `python -m scripts.mongo.py` to create the collections and add the data.  (required for testing).

NOTE: you may need to change the URL of the mongo server depending on how your machine has allocated the IP address.

## Running the tests
To run the tests, first you'll need to start the python Flask server:

```bash
python -m main
```

This will start the server on port 5000.  You will then need to open up a seperate tab to run the pytest tests.

Then, in a separate terminal, run the tests:

```bash
pytest .
```

## Test Coverage
The tests cover four main areas:
1. Liveness: Tests that the server is running and responding to requests
2. Starting a Session: Passing in a userId and featureId to the /start endpoint indicates that a new session has started.
3. Ending a Session: Passing in a userId and featureId to the /stop endpoint indicates that a session has ended.
4. Retrieving a Session: Passing in a userId and/or featureId to the /retrieve endpoint returns the activity data for the user and/or feature.



