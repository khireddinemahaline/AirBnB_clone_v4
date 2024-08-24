#!/usr/bin/python3
"""Holds the Amenity class for managing amenities.

The `Amenity` class represents an amenity that can be associated with a place.
It is designed to work with both database and file storage systems.

Attributes:
    __tablename__ (str): SQLAlchemy table name for amenities.
    name (str): Name of the amenity. Used only in database storage.
    place_amenities (relationship): SQLAlchemy relationship with
    `Place` if
    using database storage.

Conditional:
    - If `HBNB_TYPE_STORAGE` is 'db', `name` is a SQLAlchemy column and
      `place_amenities` defines the relationship with `Place`.
    - If `HBNB_TYPE_STORAGE` is not 'db', `name` is a plain string.
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Represents an amenity in the storage system.

    Inherits from BaseModel and Base to integrate with SQLAlchemy ORM if
    using database storage. The class manages amenities that can be associated
    with places.
    """

    # Table name in the database
    __tablename__ = 'amenities'

    # Conditional logic for handling storage type
    if getenv("HBNB_TYPE_STORAGE") == "db":
        # If using database storage:
        # 'name' is a column in the 'amenities' table
        name = Column(String(128), nullable=False)

        # Define a relationship with 'Place' through an association table
        place_amenities = relationship("Place", secondary=place_amenity,
                                       back_populates="amenities")
    else:
        # If using file storage:
        # 'name' is a simple string attribute
        name = ""
