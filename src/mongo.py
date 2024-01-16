from pymongo import MongoClient


class MongoConnector:
    def __init__(self, host: str, port: int, db_name: str):
        """
        Initialize a MongoConnector object.

        Args:
            host (str): host name of the MongoDB server
            port (int): port number of the MongoDB server
            db_name (str): name of the database to connect to
        """
        self._client = MongoClient(host, port)
        self._db = self._client[db_name]
        
    def create_collection(self, collection_name: str, **kwargs):
        """
        Create a collection in the database.

        Args:
            collection_name (str): collection name to create
        """
        return self._db.create_collection(collection_name, **kwargs)

    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists in the database.

        Args:
            collection_name (str): collection name to check

        Returns:
            bool: True if the collection exists, False otherwise
        """
        return collection_name in self._db.list_collection_names()
    
    def add_document(self, collection_name: str, document: dict):
        """
        Add a document to a collection.

        Args:
            collection_name (str): collection name to add the document to
            document (dict): document to add to the collection
        Error:
            ValueError: if the collection does not exist
        """
        if not self.collection_exists(collection_name):
            raise ValueError(f"Collection {collection_name} does not exist.")
        
        return self._db[collection_name].insert_one(document)
    
    def query_collection(self, collection: str, query: dict):
        """
        Query a collection.

        Args:
            collection (str): collection to query
            query (dict): query to perform

        Returns:
            list: a list of documents matching the query
        """
        return list(self._db[collection].find({key: {'$in': values} for key, values in query.items()}
))

    def get_db(self):
        return self._db
