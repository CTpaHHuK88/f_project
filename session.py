"""
Создаём подлючение к базе данных.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///db/database.db", echo=True)
session = Session(engine, future=True)