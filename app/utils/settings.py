"""
Centralized configuration management using Pydantic Settings.
All environment variables are loaded from .env file.
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

import mariadb

import pymongo
from pymongo.errors import ConnectionFailure

# Load Environment variables from .env file for local development
load_dotenv(override=True)

logger = logging.getLogger(__name__)

class Settings:
    """ A Simple class to hold environment settings """

    def __init__(self):
        # logging configs
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_level: int = getattr(logging, log_level_str, logging.INFO)

        self.db_host: str | None = os.getenv("DB_HOST")
        self.db_port: int = int(os.getenv("DB_PORT", "3306"))
        self.db_user: str | None = os.getenv("DB_USER")
        self.db_pass: str | None = os.getenv("DB_PASS")
        self.database: str | None = os.getenv("DATABASE")

        # Mongodb Settings
        self.mongo_host: str | None = os.getenv("MONGO_HOST")
        self.mongo_port: int = int(os.getenv("MONGO_PORT", "27017"))
        self.mongo_user: str | None = os.getenv("MONGO_USER")
        self.mongo_pass: str | None = os.getenv("MONGO_PASS")
        self.mongo_db:str | None = os.getenv("MONGO_DB")
        
    def get_mariadb_cursor(self):
        try:
            conn = mariadb.connect(
                user=self.db_user,
                password=self.db_pass,
                host=self.db_host,  # e.g., "localhost" or an IP address
                port=self.db_port,             # Default MariaDB port
                database=self.database
            )
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return e
        
    def get_database(self):
        # Replace the placeholder with your MongoDB connection string
        CONNECTION_STRING = f"mongodb://{self.mongo_user}:{self.mongo_pass}@{self.mongo_host}:{self.mongo_port}/?authSource={self.mongo_db}"
        try:
            # Create a connection using MongoClient
            client = pymongo.MongoClient(CONNECTION_STRING)
            
            # Check the connection (optional, but good for verification)
            client.admin.command('ping') 
            print("MongoDB connection successful!")

            # Specify the database you want to work with (e.g., 'user_data')
            # MongoDB creates the database implicitly when you first add data to it
            return client[self.mongo_db]

        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            return None
            

# Singleton instance for settings
settings = Settings()
