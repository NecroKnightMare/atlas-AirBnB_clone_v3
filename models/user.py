#!/usr/bin/python3
""" user class
that inherits from basemodel and base
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models



class User(BaseModel, Base):
    '''
    creating a table naming it users
    columns for email, password, first and last name.
    All attributes are strings
    email and password cannot be nullable
    while first and last name can be null
    '''

    __tablename__ = 'users'

    if models.storage_type == 'db':
        email = Column(
                String(128),
                nullable=False)

        password = Column(
                String(128),
                nullable=False)

        first_name = Column(
                String(128),
                nullable=True)

        last_name = Column(
                String(128),
                nullable=True)

        places = relationship(
                "Place",
                cascade="all, delete-orphan")

        reviews = relationship(
                "Review",
                cascade="all, delete-orphan")

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        @property
        def places(self):
            from models import storage
            from models.place import Place
            all_places = storage.all(Place)
            user_places = []
            for place in all_places.values():
                if places.user_id == self.id:
                    user_places.append(place)
            return user_places

        @property
        def reviews(self):
            from models import storage
            from models.review import Review
            all_reviews = storage.all(Review)
            user_reviews = []
            for review in all_reviews.values():
                if review.user_id == self.id:
                    user_reviews.append(review)
            return user_reviews
