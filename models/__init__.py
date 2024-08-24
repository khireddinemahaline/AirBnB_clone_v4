#!/usr/bin/python3
"""Initializes the storage system for the application.

This module sets up the storage system, which can either be a file-based
storage or a database-based storage, depending on the environment conf.
It also imports the necessary model classes and prepares the storage system
for use.

The `classes` dictionary maps class names to class objects for easy access.

Storage options:
    - If the environment variable `HBNB_TYPE_STORAGE` is set to 'db',
      the application will use `DBStorage` for database storage.
    - Otherwise, it defaults to `FileStorage` for file-based storage.

Imports:
    - `FileStorage`: Class for file-based storage.
    - `DBStorage`: Class for database-based storage.
    - `Amenity`, `City`, `Place`, `Review`, `State`, `User`:
    Model classes used in the application.
    - `getenv`: Function to get environment variables.

Setup:
    - `classes` dictionary maps string names of models to their respective
    classes.
    - Initializes `storage` as an instance of `DBStorage`
    if `HBNB_TYPE_STORAGE` is 'db',
      otherwise initializes `storage` as an instance of `FileStorage`.
    - Calls `storage.reload()` to load the data from the storage system
    into memory.
"""


from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

if getenv("HBNB_TYPE_STORAGE") == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
