#!/usr/bin/python3
"""Contains the Review module"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Defines class Review with public class attributes
        that return an empty string"""

    place_id = ""
    user_id = ""
    text = ""
