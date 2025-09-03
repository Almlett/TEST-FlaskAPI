# -*- coding: utf-8 -*-
"""Database connection and session management.

This module initializes the database connection using SQLAlchemy, creating an
engine and a session factory for use throughout the application. It also
provides a declarative base for ORM models.

Attributes:
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine that provides
        connectivity to the database, configured from application settings.
    SessionLocal (sqlalchemy.orm.session.sessionmaker): A factory for creating
        new database session objects to interact with the database.
    Base (sqlalchemy.ext.declarative.api.DeclarativeMeta): A declarative base
        class for ORM models. Application models should inherit from this class.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
