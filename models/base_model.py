#!/usr/bin/python3
"""
Contains BaseModel - Module, BaseModel Parent class
    serialization/deserialization information
"""

import models
from datetime import datetime
from uuid import uuid4


class BaseModel():
    """
    Defines all common attributes/methods for other classes.
    Takes care of the initialization and serialization/deserialization
    process of instances
    """
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        date_form = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, date_form)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def __str__(self):
        """Returns the str representation of a BaseModel instance"""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)

    # def __repr__(self):
    # """Returns the string representation of class BaseModel"""
    # return ("[{}] ({}) {}".format(self.__class__.__name__,
    #                                  self.id, self.__dict__))

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of
            __dict__ of the instance
        """
        newDct = self.__dict__.copy()
        newDct["__class__"] = self.__class__.__name__
        newDct["created_at"] = self.updated_at.isoformat()
        newDct["updated_at"] = self.created_at.isoformat()

        return (newDct)
