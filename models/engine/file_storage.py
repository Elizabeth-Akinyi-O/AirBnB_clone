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
        return (self.__objects)

    def new(self, obj):
        """ Creates a new object """

        Key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[Key] = value_dict

    def save(self):
        """ Saves to a file in json format """
        myObjDict = {}
        for key, val in FileStorage.__objects.items():
            myObjDict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(myObjDict, fd)

    def reload(self):
        """ Loads from json file """
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                className = val["__class"]
                className = models.classes[className]
                FileStorage.__objects[key] = className(**val)
        except FileNotFoundError:
            pass
