#!/usr/bin/python3
"""
FileStorage module

Defines the `FileStorage` class for storing and retrieving objects
in a JSON file. Provides methods to manage, persist, and handle
objects in the file system.
"""

import models
import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity


class FileStorage:
    """
    Manages object storage in a JSON file.

    Attributes:
        __file_path (str): Path to the JSON file where objects are stored.
        __objects (dict): Dictionary of all objects stored in memory.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects or objects of a specified class.

        Args:
            cls (type or str, optional):
                Class type or name to filter objects by.

        Returns:
            dict: Dictionary with keys as "<class name>.<object id>"
                  and values as object instances.
        """
        if cls:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to storage.

        Args:
            obj (BaseModel): Object to be added.
        """
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        Saves all objects to the JSON file.

        Serializes __objects to JSON format and writes to __file_path.
        """
        with open(FileStorage.__file_path, 'w', encoding="UTF-8") as f:
            my_dict = {}
            my_dict.update(FileStorage.__objects)
            for key, value in my_dict.items():
                my_dict[key] = value.to_dict()
            json.dump(my_dict, f)

    def reload(self):
        """
        Loads data from JSON file and deserializes into __objects.

        Reads JSON file and creates objects based on file data.
        """
        try:
            with open(self.__file_path, 'r') as f:
                FileStorage.__objects = json.load(f)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes an object from storage.

        Args:
            obj (BaseModel, optional): Object to be deleted.
        """
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        """
        Closes storage by calling reload().

        Reloads the data, deserializing the JSON file.
        """
        self.reload()

    def get(self, cls, id):
        """
        get the object dependes on the id
        cls.id => get this object from the storage
        """
        get_dic = self.all(cls)
        for key, value in get_dic.items():
            if key == cls.__name__ + '.' + id:
                return value
        return None

    def count(self, cls=None):
        """
        count the number of object have:
            if cls : objects with the same class name
            else : all object in the storage
        """
        count = 0
        if cls:
            get_dic = self.all(cls)
            for keys, value in get_dic.items():
                key = keys.split('.')[0]
                if key == str(cls.__name__):
                    count = count + 1
            return count
        else:
            get_dic = self.all()
            for keys, value in get_dic.items():
                count = count + 1
            return count
