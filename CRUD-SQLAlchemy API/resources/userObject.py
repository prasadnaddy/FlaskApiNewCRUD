import sqlite3          #for the sqlite operations
from flask_restful import Resource      #for creating the API resources
import uuid         #module for generating unique User ID for the users while registration
from flask import request       #module for accepting the JSON request from API
from models.users import UserModel      #importing the user model from models
from db import db           #for sqlalchemy operations

class UserRegister(Resource):       #endpoint resource for the users registration
    def post(self):     #POST Method to send the user details
        body = request.get_json()    
        user = UserModel.getUserByUserName(UserModel,body['username'])
        if not user:      #if records are present, then dont create the user
            if body['username']!='' and body['password']!='':        #checking for required fields
                uniqueID = str(uuid.uuid4())        #generating unique user IDs for each user
                userobject = UserModel(body['username'],body['password'],uniqueID)  #send the request params to model
                userobject.uniqueid = uniqueID
                db.session.add(userobject)      #add the userobject from model to database and commit changes
                db.session.commit()
                return {
                    'success':'user created successfully with unique ID: {}'.format(uniqueID)
                },201
            return {
                'error' : 'Either Username or password was not supplied'
            },404
        else:
            return{
                'error':'user already exists with name: {}'.format(body['username'])
            },403
        