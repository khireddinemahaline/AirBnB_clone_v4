#!/usr/bin/python3
"""This is the state class

This module defines the `State` class, which represents a state in the system.
The class is designed to work with both database and file storage systems.

Dependencies:
- models: For interacting with the storage system.
- sqlalchemy: For SQLAlchemy ORM support.
- os: For accessing environment variables.

Attributes:
    __tablename__ (str): The name of the table in the database.
    name (str): The name of the state. Used only in database storage.
    cities (relationship): Defines the relationship with the `City` class in
    database storage.

Conditional:
    - If `HBNB_TYPE_STORAGE` is 'db', SQLAlchemy columns and relationships
    - If `HBNB_TYPE_STORAGE` is not 'db', properties and manual handling
    objects are used.
"""

from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import shlex
import models


class State(BaseModel, Base):
    """This is the class for State

    Represents a state in the system, including its name and related cities.

    Attributes:
        name (str): The name of the state. Used only in database storage.
        cities (relationship): A list of `City` objects related to this state.
    """
    __tablename__ = 'states'  # Table name in the database

    # Define attributes based on storage type
    if getenv("HBNB_TYPE_STORAGE") == "db":
        # In database storage, use SQLAlchemy columns and relationships
        name = Column(String(128), nullable=False)  # Name of the state
        cities = relationship("City", cascade='all, delete, delete-orphan',
                              backref="state")  # Relationship with City class

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def cities(self):
            """
            Property that returns a list of `City` objects

            In file storage, manually filter and return rela city objects.

            Returns:
                list: A list of `City` objects
                where the state_id matches the state's id.
            """
            from models.city import City
            list_cities = []
            all_cities = models.storage.all(City)
            for key, city_obj in all_cities.items():
                if city_obj.state_id == self.id:
                    list_cities.append(city_obj)
            return list_cities
