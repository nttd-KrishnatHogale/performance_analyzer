"""
database/db_manager.py
"""

from backend.database.database import Database
from backend.database.models import Base


class DatabaseManager:

    @staticmethod
    def initialize():

        engine = Database.get_engine()

        Base.metadata.create_all(engine)

        print("Database initialized successfully.")