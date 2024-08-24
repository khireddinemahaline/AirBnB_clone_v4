#!/usr/bin/python3
"""Place Class

This module defines the `Place` class, which represents a place in the
context of a database or file storage system. The `Place` class includes
attributes related to a place, such as its location, description, and
amenities. It also defines relationships with other models.

Dependencies:
- models: For accessing the storage system.
- sqlalchemy: For SQLAlchemy ORM support.
- os: For accessing environment variables.

Attributes:
    __tablename__ (str): The name of the table in the database.
    city_id (str): Foreign key linking the place to a city. Used only in
    database storage.
    user_id (str): Foreign key linking the place to a user. Used only in
    database storage.
    name (str): The name of the place. Used only in database storage.
    description (str): A description of the place. Used only in database
    storage.
    number_rooms (int): The number of rooms in the place. Used only in
    database storage.
    number_bathrooms (int): The number of bathrooms in the place. Used only
    in database storage.
    max_guest (int): The maximum number of guests allowed. Used only in
    database storage.
    price_by_night (int): The price per night. Used only in database storage.
    latitude (float): The latitude of the place. Used only in database
    storage.
    longitude (float): The longitude of the place. Used only in database
    storage.
    reviews (relationship): SQLAlchemy relationship with `Review` model.
    amenities (relationship): SQLAlchemy relationship with `Amenity` model
    if using database storage.

Conditional:
    - If `HBNB_TYPE_STORAGE` is 'db', use SQLAlchemy columns and
    relationships.
    - If `HBNB_TYPE_STORAGE` is not 'db', use plain attributes and define
    properties for reviews and amenities.
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

# Many-to-many relationship table between Place and Amenity
place_amenity = Table("place_amenity", Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id', onupdate='CASCADE',
                                        ondelete='CASCADE'),
                             primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey("amenities.id",
                                        onupdate='CASCADE',
                                        ondelete='CASCADE'),
                             primary_key=True))


class Place(BaseModel, Base):
    """Place Class

    Represents a place that can have various attributes and associations
    with other models. The class includes SQLAlchemy columns and relationships
    for database storage and properties for file storage.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        city_id (str): Foreign key linking to the city. Used in dbstorage.
        user_id (str): Foreign key linking to the user. Used in dbstorage.
        name (str): The name of the place. Used in database storage.
        description (str): Description of the place. Used in database storage.
        number_rooms (int): Number of rooms in the place. Used in dbstorage.
        number_bathrooms (int): Number of bathrooms in the place.
        max_guest (int): Maximum number of guests allowed. Used in dbstorage.
        price_by_night (int): Price per night. Used in database storage.
        latitude (float): Latitude of the place. Used in database storage.
        longitude (float): Longitude of the place. Used in database storage.
        reviews (relationship): Relationship with `Review` model for dbstorage.
        amenities (relationship): Rela with `Amenity` model for dbstorage.

    Conditional:
        - If `HBNB_TYPE_STORAGE` is 'db', use SQLAlchemy
        columns and relationships.
        - If `HBNB_TYPE_STORAGE` is not 'db', use plain attributes
        and define
          properties for reviews and amenities.
    """
    __tablename__ = 'places'  # Table name in the database

    # Define attributes and relationships based on storage type
    if getenv("HBNB_TYPE_STORAGE") == "db":
        # In database storage, use SQLAlchemy columns and relationships
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)
        # Relationship with Review model
        reviews = relationship("Review", backref="place")
        # Relationship with Amenity model
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        # In file storage, use plain attributes and define properties
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = {}

        @property
        def reviews(self):
            """List reviews for the place.

            Returns:
                list: List of `Review` instances associated with this place.
            """
            from models.review import Review
            list_reviews = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    list_reviews.append(review)
            return list_reviews

        @property
        def amenities(self):
            """List amenities for the place.

            Returns:
                list: List of `Amenity` instances associated with this place.
            """
            from models.amenity import Amenity
            all_amenity = list(models.storage.all(Amenity).values())
            list_amenities = [a for a in all_amenity if a.place_id == self.id]
            return list_amenities

        @amenities.setter
        def amenities(self, amenity=None):
            """Set amenities for the place.

            Args:
                amenity (Amenity): An instance of `Amenity` to add to the list.
            """
            if amenity:
                for amenity in models.storage.all(Amenity).values():
                    if amenity.place_id == self.id:
                        amenity_ids.append(amenity)
