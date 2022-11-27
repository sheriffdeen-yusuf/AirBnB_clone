'''File STroge engine that serializes instances to a JSON file and deserializes JSON file to instances:'''

import json

def obj_encode_hook(obj):
    try:
        obj_cls  = obj['__class__']
    except KeyError:
        return obj
    else:
        try:
            return getattr(obj_cls)(**obj)
        except AttributeError:
            return obj



class FileStroage():
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj.dict()

    def save(self):
        all_objs = {}
        for key in self.__objects:
            all_objs[key] = self.__objects[key].to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(all_objs, f)
    
    def reload(self):
        try:
            with open(self.__file_path, 'r') as f:
                self.__objects = json.load(f, object_hook="obj_encode_hook")
        except:
            pass