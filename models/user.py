#!/usr/bin/python3
""" holds class User

This module defines the `User` class, which represents a user in the system.
The class is designed to work with both database and file storage systems.

Dependencies:
- models: For interacting with the storage system.
- sqlalchemy: For SQLAlchemy ORM support.
- os: For accessing environment variables.

Attributes:
    __tablename__ (str): The name of the table in the database.
    email (str): The email address of the user. Used only in database storage.
    password (str): The password of the user. Used only in database storage.
    first_name (str): The first name of the user. Optional, used in dbstorage.
    last_name (str): The last name of the user. Optional, used in dbstorage.
    places (relationship): Defines the relationship with the `Place` class in
    database storage. Specifies how to handle related `Place` objects.
    reviews (relationship): Defines the relationship with the `Review` class in
    database storage. Specifies how to handle related `Review` objects.

Conditional:
    - If `HBNB_TYPE_STORAGE` is 'db', columns and relationships are used.
    - If `HBNB_TYPE_STORAGE` is not 'db', attributes are defined as strings.
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user

    Represents a user in the system,
    including personal details and relationships
    with places and reviews.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        places (relationship): Relationship with `Place` objects,
                                specifying how
                               `Place` objects are associated with this user.
        reviews (relationship): Relationship with `Review` objects,
                                specifying how
                                `Review` objects are associated with this user.
    """
    __tablename__ = 'users'  # Table name in the database

    # Define attributes based on storage type
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        # In database storage, use SQLAlchemy columns and relationships
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        # Relationship with Place class
        places = relationship("Place", backref='user',
                              cascade="all, delete, delete-orphan")
        # Relationship with Review class
        reviews = relationship("Review", backref='user',
                               cascade="all, delete, delete-orphan")

    else:
        # In file storage, attributes are plain strings
        email = ""  # User's email address
        password = ""  # User's password
        first_name = ""  # User's first name (optional)
        last_name = ""  # User's last name (optional)
