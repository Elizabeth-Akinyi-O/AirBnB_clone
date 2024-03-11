#!/usr/bin/python3
"""Contains the User module"""
from models.base_model import BaseModel


class User(BaseModel):
    """Defines the User class with public class attributes
        that return an empty string"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
