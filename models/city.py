#!/usr/bin/python3
"""Holds the City class for managing cities.

The `City` class represents a city and is designed to work with both
database and file storage systems. It defines attributes and relationships
for cities, including their name and association with a state.

Dependencies:
- models: For accessing the storage system.
- sqlalchemy: For SQLAlchemy ORM support.
- os: For accessing environment variables.

Attributes:
    __tablename__ (str): SQLAlchemy table name for cities.
    name (str): Name of the city. Used only in database storage.
    state_id (str): Foreign key linking the city to a state. Used only in
    database storage.
    places (relationship): SQLAlchemy relationship with `Place` if using
    database storage.
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from os import getenv
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of a city.

    This class maps to the 'cities' table in the database. It includes
    attributes for the city's name and its association with a state.
    It also defines a relationship with the `Place` model if using
    database storage.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (str): The name of the city. This attribute is used only in
        database storage.
        state_id (str): The ID of the state to which the city belongs. This
        attribute is used only in database storage.
        places (relationship): The relationship with the `Place` model. It
        allows accessing all places associated with this city and defines
        cascading options for delete operations.
    """
    __tablename__ = 'cities'  # Table name in the database

    # Define attributes and relationships based on storage type
    if getenv("HBNB_TYPE_STORAGE") == "db":
        # In database storage, use SQLAlchemy columns
        name = Column(String(128), nullable=False)  # City name
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        # Foreign key to state
        # Relationship with Place model
        places = relationship("Place", backref="cities",
                              cascade="all, delete, delete-orphan")
    else:
        # In file storage, use simple attributes
        state_id = ""  # Foreign key to state
        name = ""  # City name
