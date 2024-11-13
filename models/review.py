#!/usr/bin/python3
"""
Review class that inherits from BaseModel and Base
"""


from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey, Column, String
import models

class Review(BaseModel, Base):
    """
    Review class that inherits from BaseModel
    Tablename called reviews

    Public class attributes:
        Column: place_id: a string of up to 1024 char
                linked to places.id and cannot be null
        Column: user_id: string of 60 char
                linked to users.id and cannot be null
        Column: text: string of 1024 char and cannot be null
    """
    __tablename__ = 'reviews'

    if models.storage_type == 'db':
        text = Column(
                String(1024),
                nullable=False)

        place_id = Column(
            String(60),
            ForeignKey('places.id'),
            nullable=False)

        user_id = Column(
            String(60),
            ForeignKey('users.id'),
            nullable=False)
    else:
        text = ""
        place_id = ""
        user_id = ""
