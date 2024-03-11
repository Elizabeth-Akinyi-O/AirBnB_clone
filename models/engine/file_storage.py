#!/usr/bin/python3
""" Engine that is incharge of serializing/deserializing objects to files """
import json
import os


class FileStorage():
    """ Serialization/Deserialization of data """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns dictionaries """
        return (FileStorage.__objects)

    def new(self, obj):
        """ Creates a new object """
        className = type(obj).__name__
        myId = obj.id
        instanceKey = className + "." + myId
        FileStorage.__objects[instanceKey] = obj

    def save(self):
        """ Saves to a file in json format """
        myObjDict = {}
        for key in FileStorage.__objects:
            myObjDict[key] = FileStorage.__objects[key].to_dict()
        with open(FileStorage.__file_path, 'w') as file_path:
            json.dump(myObjDict, file_path)

    def reload(self):
        """ Loads from json file """
        from models.base_model import BaseModel
        from models.amenity import Amenity
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.review import Review
        myDict = {
            "BaseModel": BaseModel,
            "Amenity": Amenity,
            "User": User,
            "State": State,
            "City": City,
            "Place": Place,
            "Review": Review
            }
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, 'r') as file_path:
            objects = json.load(file_path)
            FileStorage.__objects = {}
            for key in objects:
                name = key.split(".")[0]
                FileStorage.__objects[key] = myDict[name](**objects[key])
