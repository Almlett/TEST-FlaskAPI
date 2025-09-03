# -*- coding: utf-8 -*-
"""Database connection and session management.

This module initializes the database connection using SQLAlchemy. It configures the
database engine and a session factory for creating database sessions throughout the
application.

Attributes:
    DATABASE_URL (str): The connection string for the database, retrieved from
        the "DATABASE_URL" environment variable.
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine that provides
        connectivity to the database.
    SessionLocal (sqlalchemy.orm.session.sessionmaker): A factory for creating
        new database session objects. These sessions are used to interact with
        the database.
    Base (sqlalchemy.ext.declarative.api.DeclarativeMeta): A declarative base
        class for ORM models. All application models should inherit from this
        class to be mapped to the database.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

