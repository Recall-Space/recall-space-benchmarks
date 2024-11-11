"""
Connector to database management. For recall space Mongo database.
"""

import os
from pymongo import MongoClient


class MongoConnector:
    """
    Handles interactions with the MongoDB database.

    Attributes:
        client (MongoClient): The MongoDB client.
        db (Database): The MongoDB database.
        collection (Collection): The MongoDB collection for storing chat sessions.
    """

    def __init__(
        self, db_name, collection_name, uri=os.getenv("MONGO_DB_CONNECTION_STRING")
    ):
        """
        Initializes the MongoDBHandler with the specified database and collection.

        Args:
            db_name (str): The name of the database.
            collection_name (str): The name of the collection.
            uri (str): The MongoDB connection string.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_session(self, session_data):
        """
        Inserts a chat session document into the collection.

        Args:
            session (dict): The chat session document to be inserted.
        """
        query = {"user": session_data["user"], "session": session_data["session"]}

        update = {
            "$set": {
                "participant_2": session_data["participant_2"],
                "timestamp": session_data["timestamp"],
                "list_messages": session_data["list_messages"],
            }
        }
        # Update the document if it exists, otherwise insert a new one
        self.collection.update_one(query, update, upsert=True)

    def delete_session(self, session):
        query = {"session": session}
        self.collection.delete_many(query)

    def get_session(self, user, session):
        """
        Retrieves a chat session by its session ID.

        Args:
            session (str): The session ID to filter sessions by.

        Returns:
            dict: The chat session document or None if not found.
        """
        query = {"user": user, "session": session}
        # Only include "list_messages" field in the result, exclude "_id" and other fields
        projection = {"list_messages": 1, "_id": 0}
        result = self.collection.find_one(query, projection)
        if result:
            return result["list_messages"]
        else:
            return []
