#!/usr/bin/python3
"""
Contains BaseModel - Module, BaseModel Parent class
    serialization/deserialization information
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel():
    """
    Defines all common attributes/methods for other classes.
    Takes care of the initialization and serialization/deserialization
    process of instances
    """
    def __init__(self, *args, **kwargs):
        """Initialization of a BaseModel instance"""
        if kwargs:
            dateformat = "%Y-%m-%dT%H:%M:%S.%f"
            k_dict = kwargs.copy()
            del k_dict["__class__"]
            for key in k_dict:
                if (key == "created_at" or key == "updated_at"):
                    k_dict[key] = datetime.strptime(k_dict[key], date_format)
            self.__dict__ = k_dict
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """String representation of a BaseModel instance"""
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def __repr__(self):
        """Returns the string representation of class BaseModel"""
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of
            __dict__ of the instance
        """
        newDct = self.__dict__.copy()
        newDct['__class__'] = self.__class__.__name__
        newDct['created_at'] = self.updated_at.isoformat()
        newDct['updated_at'] = self.created_at.isoformat()

        return (newDct)
