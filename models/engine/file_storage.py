#!/usr/bin/python3

"""A module that contains attributes
and methods for serialisation and
deserialization of JSON data"""
import datetime

import models
import json
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def models_encod_hook(obj):
    """Returns an instance of a generated json string literal"""
    try:
        cls = obj['__class__']
    except KeyError:
        return obj
    else:
        try:
            return getattr(models, cls)(**obj)
        except AttributeError:
            return obj


class FileStorage:
    """serializes instances to a
    JSON file & deserializes back
    to instances"""

    # string - path to the JSON file (ex: file.json)
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self):
        """Return all the objects saved in the file"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def save(self):
        """serialises __objects to the JSON file"""
        json_objects = {}
        filename = self.__file_path
        for keys in self.__objects:
            json_objects[keys] = self.__objects[keys].to_dict()
        with open(filename, mode='w', encoding='utf-8') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        filename = self.__file_path
        try:
            with open(filename, mode='r', encoding='utf-8') as rf:
                self.__objects = json.load(rf, object_hook=models_encod_hook)
        except FileNotFoundError:
            pass

    def classes(self):
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        class_dict = {
            'BaseModel': BaseModel}
        return class_dict
      
    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel":
                {"id": str,
                 "created_at": datetime.datetime,
                 "updated_at": datetime.datetime}
        }
        return attributes