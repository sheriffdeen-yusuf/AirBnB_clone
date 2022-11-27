
'''
The BaseModel is the base classes where other class inherits from
'''
import uuid
from datetime import datetime
from __init__ import storage

class BaseModel:
    '''class BaseModel that defines all common attributes/methods for other classes'''
    
    def __init__(self, *args, **kwargs):
        '''init'''
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if bool(kwargs) is False:
            storage.new(self)
        
    def save(self):
        self.updated_at = datetime.now()
        storage.save()
    
    def to_dict(self):
        my_dict = self.__dict__
        my_dict['__class__'] =  str(self.__class__.__name__)
        my_dict['updated_at'] = self.updated_at.isoformat()
        my_dict['created_at'] = self.created_at.isoformat()
        
        return my_dict
        
    def __str__(self):
        name = self.__class__.__name__
        id = self.id
        class_dict = self.__dict__
        return "[{}] ({}) {}".format(name, id, class_dict)


