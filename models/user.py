#!/usr/bin/python3
''' The User class'''

from models.base_model import BaseModel

class User(BaseModel):
    ''' contains public attributes of email, passwors, fname and lname'''
    email = ""
    password = ""
    first_name = ""
    last_name = ""
