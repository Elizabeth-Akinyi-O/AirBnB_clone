#!/usr/bin/python3
"""
Console base for the unit
"""
import cmd
from models.base_model import BaseModel
from models import storage
import json
import shlex
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.palce import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command prompt to access models data"""
    prompt = "(hbnd)"
    myDict = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
            }

    def do_nothing(self, arg):
        """Does nothing"""
        pass

    def do_quit(self, arg):
        """Closes program and safely saves data"""
        return True

    def do_EOF(self, arg):
        """Closes the program and safely saves data when user
            inputs ctrl + D"""
        print("")
        return True

    def emptyline(self):
        """Overrides the empty line method"""
        pass

    def do_create(self, arg):
        """Creates a new instance of class BaseModel
        Structure: create [class name]"""

        if not arg:
            print("** class name missing **")
            return
        myData = shlex.split(arg)
        if myData[0] not in HBNBCommand.myDict.keys():
            print("** class doesn't exist **")
            return
        newInstance = HBNBCommand.myDict[myData[0]]()
        newInstance.save()
        print(newInstance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the
            class name and id
        Structure: show [class name] [id]"""

        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        if tokens[0] not in HBNBCommand.myDict.keys():
            print("** class doesn't exist **")
            return
        if len(tokens) <= 1:
            print("** instance id missing **")
            return
        storage.reload()
        objsDict = storage.all()
        key = tokens[0] + "." + tokens[1]
        if key in objsDict:
            objInstance = str(objsDict[key])
            print(objInstance)
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id, and saves the
            changes into the JSON file
        Structure: destroy [class name] [id]"""

        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        if tokens[0] not in HBNBCommand.myDict.keys():
            print("** class doesn't exist **")
            return
        if len(tokens) <= 1:
            print("** instance id missing **")
            return
        storage.reload()
        objsDict = storage.all()
        key = tokens[0] + "." + tokens[1]
        if key in objsDict:
            del objsDict[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representations of all instances based or not
            based on the class name (prints the whole file)
        Structure: all [class name] or all"""

        storage.reload()
        my_json = []
        objectsDict = storage.all()
        if not arg:
            for key in objectsDict:
                my_json.append(str(objectsDict[key]))
            print(json.dumps(my_json))
            return
        token = shlex.split(arg)
        if token[0] in HBNBCommand.myDict.keys():
            for key in objectsDict:
                if tokens[0] in key:
                    my_json.append(str(objectsDict[key]))
            print(json.dumps(my_json))
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or
            updating attribute and saves the changes into the JSON file
        Structure: update [class name] [id] [argName] [argValue]"""

        if not arg:
            print("** class name missing **")
            return
        myData = shlex.split(arg)
        storage.reload()
        objsDict = storage.all()
        if myData[0] not in HBNBCommand.myDict.keys():
            print("** class doesn't exist **")
            return
        if (len(myData) == 1):
            print("** instance id missing **")
            return
        try:
            key = myData[0] + "." + myData[1]
            objsDict[key]
        except KeyError:
            print("** no instance found **")
            return
        if (len(myData) == 2):
            print("** attribute name missing **")
            return
        if (len(myData) == 3):
            print("** value missing **")
            return
        myInstance = objsDict[key]
        if hasattr(myInstance, myData[2]):
            dataType = type(getattr(myInstance, myData[2]))
            setattr(myInstance, myData[2], dataType(myData[3]))
        else:
            setattr(myInstance, myData[2], myData[3])
        storage.save()

    def do_update2(self, arg):
        """Updates an instance based on the class name and id by adding
            or updatingattribute and saves the changes into the JSON file
        Structure: update [class name] [id] [dictionary]"""

        if not arg:
            print("** class name missing **")
            return
        myDictionary = "{" + arg.split("{")[1]
        myData = shlex.split(arg)
        storage.reload()
        objsDict = storage.all()
        if myData[0] not in HBNBCommand.myDict.keys():
            print("** class doesn't exist **")
            return
        if (len(myData) == 1):
            print("** instance id missing **")
            return
        try:
            key = myData[0] + "." + myData[1]
            objsDict[key]
        except KeyError:
            print("** no instance found **")
            return
        if (myDictionary == "{"):
            print("** attribute name missing **")
            return

        myDictionary = myDictionary.replace("\'", "\"")
        myDictionary = json.loads(myDictionary)
        myInstance = objsDict[key]
        for myKey in myDictionary:
            if hasattr(myInstance, myKey):
                dataType = type(getattr(myInstance, myKey))
                setattr(myInstance, myKey, myDictionary[myKey])
            else:
                setattr(myInstance, myKey, myDictionary[myKey])
        storage.save()

    def do_count(self, arg):
        """Counts number of instances of a class"""

        counter = 0
        objectsDict = storage.all()
        for key in objectsDict:
            if (arg in key):
                counter += 1
        print(counter)

    def default(self, arg):
        """Handles new ways of inputing data"""

        valueDict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        arg = arg.strip()
        values = arg.split(".")
        if len(values) != 2:
            cmd.Cmd.default(self, arg)
            return
        className = values[0]
        command = values[1].split("(")[0]
        line = ""
        if (command == "update" and values[1].split("(")[1][-2] == "}"):
            inputs = values[1].split("(")[1].split(",", 1)
            inputs[0] = shlex.split(inputs[0])[0]
            line = "".json(inputs)[0:-1]
            line = className + " " + line
            self.do_update2(line.strip())
            return
        try:
            inputs = values[1].split("(")[1].split(",")
            for number in range(len(inputs)):
                if (number != len(inputs) - 1):
                    line = line + " " + shlex.split(inputs[number])[0]
                else:
                    line = line + " " + shlex.split(inputs[number][0:-1])[0]
        except IndexError:
            inputs = ""
            line = ""
        line = className + line
        if (command in valueDict.keys()):
            valueDict[command](line.strip())


if __name__ = '__main__':
    HBNBCommand().cmdloop()
