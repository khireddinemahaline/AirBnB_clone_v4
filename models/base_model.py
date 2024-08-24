#!/usr/bin/python3
"""Base model that all models will inherit from.

This module defines the `BaseModel` class, which is the base class for all
models in the application. It provides common attributes and methods
for managing objects in the storage system, including ID, creation, and
update timestamps.

Dependencies:
- uuid: For generating unique identifiers.
- sqlalchemy: For SQLAlchemy ORM support.
- datetime: For managing date and time.
- models: For accessing the storage system.

Attributes:
    id (str): Unique identifier for each instance.
    created_at (datetime): Timestamp when the instance was created.
    updated_at (datetime): Timestamp when the instance was last updated.
"""

import uuid
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, String, DateTime
import models

Base = declarative_base()


class BaseModel:
    """
    BaseModel:
        id : the UUID of the class instance.
        created_at : the timestamp when the instance was created.
        updated_at : the timestamp when the instance was last updated.
    """
    # Define SQLAlchemy columns for the BaseModel
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Constructor to initialize the BaseModel instance.

        Args:
            *args: Positional arguments (not used).
            **kwargs: Keyword arguments for initializing the instance.

        The constructor generates a new UUID for `id`, and sets `created_at`
        and `updated_at` to the current time. If keyword arguments are
        provided,
        they are used to update the instance attributes.
        """
        self.id = str(uuid.uuid4())  # Generate a new UUID
        self.created_at = datetime.now()  # Set creation time
        self.updated_at = datetime.now()  # Set last update time

        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the instance.

        Returns:
            str: A string representation including class name, ID, and
            attribute values.

        This method generates a string that includes the class name, ID,
        and all attributes of the instance, except '_sa_instance_state'.
        """
        cls = type(self).__name__  # Extract class name
        attributes = ', '.join(
            "'{}': {}".format(key, repr(getattr(self, key)))
            for key in self.__dict__.keys()
            if key != '_sa_instance_state'
        )
        return "[{}] ({}) {{{}}}".format(cls, self.id, attributes)

    def save(self):
        """
        Save the current instance to the storage.

        This method updates the `updated_at` timestamp, adds the instance
        to the storage, and commits the changes.
        """
        self.updated_at = datetime.now()  # Update timestamp
        models.storage.new(self)  # Add to storage
        models.storage.save()  # Commit changes

    def to_dict(self):
        """
        Convert the instance to a dictionary representation.

        Returns:
            dict: A dictionary containing all attributes of the instance,
            including `created_at` and `updated_at` as ISO-formatted strings.

        The dictionary includes the class name under the key '__class__'.
        """
        dic_obj = {}
        dic_obj.update(self.__dict__)  # Copy instance dictionary
        if '_sa_instance_state' in dic_obj:
            del dic_obj['_sa_instance_state']  # Remove SQLAlchemy state
        dic_obj.update({
            '__class__': type(self).__name__,  # Add class name
            'created_at': self.created_at.isoformat(),  # Format date as ISO
            'updated_at': self.updated_at.isoformat()
        })
        return dic_obj

    def delete(self):
        """
        Delete the current instance from storage.

        This method removes the instance from the storage.
        """
        models.storage.delete(self)  # Remove from storage
