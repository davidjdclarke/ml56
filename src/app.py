import logging
from flask import Flask, request, jsonify
from datetime import datetime

from src.mongo import MongoConnector
from flask import request

# TODO - move these to a config file
HOST = "mongodb://172.17.0.2"
PORT = 27017
DATABASE = "ABC"

logger = logging.getLogger(__name__)

app = Flask(__name__)


class Application:
    def __init__(self):
        self._mongo_connector = MongoConnector(host=HOST, port=PORT, db_name=DATABASE)
        self._configure_routes()
    
    def run(self):
        app.run()
        
    def _configure_routes(self):
        """
        Configures the routes for the application.
        """
        app.add_url_rule("/health/liveness", view_func=self._liveness)
        app.add_url_rule("/start", view_func=self._start, methods=["POST"])
        app.add_url_rule("/stop", view_func=self._stop, methods=["POST"])
        app.add_url_rule("/retrieve", view_func=self._retrieve, methods=["GET"])
    
    def _liveness(self):
        """
        Checks the liveness of the application.

        Returns:
            A JSON response with the status of the application.
        """
        return jsonify({"status": "UP"})
    
    def _parse_activity_request(self, request_dict: dict) -> tuple:
        """
        Parses an activity request.

        Args:
            request_dict (dict): a dictionary containing the request

        Raises:
            ValueError: If the request does not contain a userId or featureId.

        Returns:
            tuple: a tuple containing the userId and featureId
        """
        user_id = request_dict.get("userId")
        feature_id = request_dict.get("featureId")
        
        if request_dict.get("userId") is None:
            raise ValueError("Missing userId in request.")
        if request_dict.get("featureId") is None:
            raise ValueError("Missing featureId in request.")
        
        return user_id, feature_id

    def _start(self):
        try:
            request_dict = request.get_json()
            logger.info(f"Received request to start activity: {request}")
            
            user_id, feature_id = self._parse_activity_request(request_dict)
            
            # Create an activity object
            activity = {
                "userId": user_id,
                "featureId": feature_id,
                "activityType": "START",
                "timestamp": datetime.now(),
                "additionalNotes": request_dict.get("additionalNotes", "")
            }
            
            # Insert the activity into the database
            self._mongo_connector.add_document("activities", activity)
            
            # Return a success response
            return jsonify({"status": "SUCCESS"})
        except Exception as e:
            logger.error(f"Error while starting activity: {e}")
            return jsonify({"status": "ERROR", "message": str(e)}), 500
    
    def _stop(self):
        """
        Stops an activity.

        Returns:
            A JSON response with the status of the request.
        """
        try:
            request_dict = request.get_json()
            logger.info(f"Received request to stop activity: {request}")
            
            user_id, feature_id = self._parse_activity_request(request_dict)
            
            # Create an activity dict
            activity = {
                "userId": user_id,
                "featureId": feature_id,
                "activityType": "STOP",
                "timestamp": datetime.now(),
                "additionalNotes": request_dict.get("additionalNotes", "")
            }
            
            # Insert the activity into the database
            self._mongo_connector.add_document("activities", activity)
            
            # Return a success response
            return jsonify({"status": "SUCCESS"})
        except Exception as e:
            logger.error(f"Error while stopping activity: {e}")
            return jsonify({"status": "ERROR", "message": str(e)}), 500
        
    def _retrieve(self):
        """
        Gets the sessions of a user or for a feature or both.

        Returns:
            A JSON response with the sessions applicable to the query.
        """
        request_dict = request.get_json()
        try:
            user_id = request_dict.get("userId")
            feature_id = request_dict.get("featureId")
            
            query = {}
            if user_id:
                query["userId"] = [user_id]
            if feature_id:
                query["featureId"] = [feature_id]
                
            response = {"result": str(self._mongo_connector.query_collection("activities", query))}
            logger.info(f"Retrieved sessions: {response}")
            return jsonify(response)
        except Exception as e:
            logger.error(f"Error while getting sessions: {e}")
            return jsonify({"status": "ERROR", "message": str(e)}), 500