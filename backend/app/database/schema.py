from sqlalchemy import Engine
from sqlmodel import SQLModel

from app.database.connections import engine as default_engine


def create_db_and_tables(override_engine: None | Engine = None):
    SQLModel.metadata.create_all(override_engine or default_engine)
