#!/usr/bin/python3
"""
Contains the DBStorage class.

Manages interactions with a MySQL database using SQLAlchemy.
Provides methods for CRUD operations and session management.
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """
    Interacts with MySQL using SQLAlchemy.

    Attributes:
        __engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine instance.
        __session(sqlalchemy.orm.scoping.scoped_session):Scoped sessionfactory.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes DBStorage instance.

        Sets up the SQLAlchemy engine and connection. Drops all tables if
        the environment is 'test'.
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db))
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all instances of a class from the database.

        Args:
            cls (type, optional): Class of objects to query.
            Queries all if None.

        Returns:
            dict: Dictionary with keys as "<class name>.<object id>" and
                  values as object instances.
        """
        db_dict = {}
        if cls is not None and cls != '':
            if isinstance(cls, str):
                cls = models.classes.get(cls)
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                if obj.__class__.__name__ in models.classes:
                    db_dict[key] = obj
            return db_dict
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    for obj in objs:
                        key = "{}.{}".format(obj.__class__.__name__,
                                             obj.id)
                        db_dict[key] = obj
        return db_dict

    def new(self, obj):
        """
        Adds a new object to the session.

        Args:
            obj (BaseModel): Object to add to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes in the session to the database.

        Saves all modified objects to the database.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the session.

        Args:
            obj (BaseModel, optional): Object to delete. No operation if None.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads data from the database and initializes the session.

        Creates tables and sets up a new scoped session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes the current database session.

        Ensures the session is properly closed.
        """
        self.__session.close()

    def get(self, cls, id):
        """
        get the object dependes on the id
        cls.id => get this object from the storage
        """
        get_dic = self.all(cls)
        for key, value in get_dic.items():
            if key == str(cls.__name__) + '.' + id:
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
