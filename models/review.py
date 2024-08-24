#!/usr/bin/python3
""" holds class Review

This module defines the `Review` class, which represents a review of a place.
The class is designed to work with both database and file storage systems.

Dependencies:
- models: For accessing the storage system.
- sqlalchemy: For SQLAlchemy ORM support.
- os: For accessing environment variables.

Attributes:
    __tablename__ (str): The name of the table in the database.
    text (str): The text of the review. Used only in database storage.
    place_id (str): Foreign key linking the review to a place. Used only in
    database storage.
    user_id (str): Foreign key linking the review to a user. Used only in
    database storage.

Conditional:
    - If `HBNB_TYPE_STORAGE` is 'db', use SQLAlchemy columns for attributes.
    - If `HBNB_TYPE_STORAGE` is not 'db', use plain attributes.
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Representation of Review

    Represents a review for a place, including the text of the review, and
    links to both the place and the user who made the review.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        text (str): The text of the review. Used only in database storage.
        place_id (str): Foreign key linking to the place being reviewed.
        user_id (str): Foreign key linking to the user who wrote the review.

    Conditional:
        - If `HBNB_TYPE_STORAGE` is 'db', SQLAlchemy columns are used to define
          attributes.
        - If `HBNB_TYPE_STORAGE` is not 'db', plain attributes are used.
    """
    __tablename__ = 'reviews'  # Table name in the database

    # Define attributes based on storage type
    if getenv("HBNB_TYPE_STORAGE") == "db":
        # In database storage, use SQLAlchemy columns
        text = Column(String(1024), nullable=False)  # Review text
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        # In file storage, use plain attributes
        place_id = ""  # Foreign key to Place
        user_id = ""  # Foreign key to User
        text = ""  # Review text
