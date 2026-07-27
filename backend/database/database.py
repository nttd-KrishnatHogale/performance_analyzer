"""
database/database.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from config.config_service import ConfigService


class Database:

    _engine = None
    _Session = None

    @classmethod
    def initialize(cls):

        if cls._engine:
            return

        config = ConfigService()
        project_root = Path(__file__).resolve().parents[2]

        db_name = config.get("database.name")
        db_file = project_root / db_name

        db_file.parent.mkdir(parents=True, exist_ok=True)

        # db_path = Path("database") / db_name

        db_url = f"sqlite:///{db_file}"

        cls._engine = create_engine(
            db_url,
            # echo=config.get("database.echo"),
            echo=False,
            future=True
        )

        cls._Session = sessionmaker(
            bind=cls._engine,
            autoflush=False,
            autocommit=False
        )

    @classmethod
    def get_engine(cls):

        if cls._engine is None:
            cls.initialize()

        return cls._engine

    @classmethod
    def get_session(cls):

        if cls._Session is None:
            cls.initialize()

        return cls._Session()