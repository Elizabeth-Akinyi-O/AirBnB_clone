#!/usr/bin/python3
"""Contains the Place module"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Defines class Place with public class attributes
        that return an empty string"""
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
