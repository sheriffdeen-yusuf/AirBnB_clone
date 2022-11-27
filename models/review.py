#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    ''' Class Review accepts place_id, user_id and tezt attribute. '''

    place_id = ""
    user_id = ""
    text = ""
