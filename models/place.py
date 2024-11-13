#!/usr/bin/python3
"""
Place class that inherits from BaseModel and Base
"""

from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False))


class Place(BaseModel, Base):
    """
    Table name: places

    Public class attributes:
        Column: city_id - string of 60 char
                it will be the City.id cannot be null
        Column: user_id - string of 60 char
                it will be the User.id cannot be null
        Column: name - string of 128 char, cannot be null
        Column: description - string 1024 char, can be null
        Column: number_rooms - integer, defaults to 0
                cannot be null
        Column: number_bathrooms - integer, defaults to 0
                cannot be null
        Column: max_guest - integer, defaults to 0
                cannot be null
        Column: price_by_night - integer, defaults to 0
                cannot be null
        Column: latitude - float, can be null
        Column: longitude- float, can be null

        amenity_ids: list of string -
            empty list: it will be the list of Amenity.id later
    """

    __tablename__ = 'places'

    if BaseModel.storage_type == 'db':
        city_id = Column(
                String(60),
                ForeignKey('cities.id'),
                nullable=False)

        user_id = Column(
                String(60),
                ForeignKey('users.id'),
                nullable=False)

        name = Column(
                String(128),
                nullable=False)

        description = Column(
                String(1024),
                nullable=True)

        number_rooms = Column(
                Integer,
                default=0,
                nullable=False)

        number_bathrooms = Column(
                Integer,
                default=0,
                nullable=False)

        max_guest = Column(
                Integer,
                default=0,
                nullable=False)

        price_by_night = Column(
                Integer,
                default=0,
                nullable=False)

        latitude = Column(
                Float,
                nullable=True)

        longitude = Column(
                Float,
                nullable=True)

        amenities = relationship(
                'Amenity',
                secondary=place_amenity,
                viewonly=False)

        reviews = relationship(
                "Review",
                cascade="all, delete-orphan")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def amenities(self):
        from models import storage
        from models.amenity import Amenity
            all_amenities = storage.all(Amenity)
            place_amenities = []
            for amenity in all_menities.values():
                if amenity.id in amenity_ids:
                    place_amenities.append(amenity)
            return place_amenities

    @property
    def reviews(self):
        from models import storage
        from models.review import Review
            all_reviews = storage.all(Review)
            place_reviews = []
        for review in all_reviews.values():
                if review.place_id == self.id:
                    place_reviews.append(review)
        return place_reviews

    @amenities.setter
    def amenities(self, amenity):
        from models import Amenity
        if (isinstance(amenity, Amenity) and
            amenity.id not in self.amenity_ids):
            amenity_ids.append(amenity.id)
