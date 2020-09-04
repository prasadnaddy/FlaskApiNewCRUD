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
        
class User(Resource):                   #endpoint resource for performing action such as GET, DELETE on users model
    def get(self, _id):          #GET method to get the user's information
        user = UserModel.getUserByID(UserModel, _id)        #getting the user's information by passing user ID
        if not user:        #if we dont get any user object based on userID
            return {
                'Error' : 'The provided user ID is not valid, please check again'
            },404       #return error message with 404 Response
        return {
            'UserDetails' : {
                'Name' : user.username,
                'UniqueID': user.uniqueid,
            }           #return the user object as json with 200 status code
        },200
    
    def delete(self, _id):       #DELETE method to delete the user's information
        user = UserModel.getUserByID(UserModel,_id)        #getting the user's information by passing User ID
        if not user:        #if user object is not returned, then throw not found error with 404 status code
            return {
                'Error' : 'The provided user ID is not valid, please check again'
            },404
        db.session.query(UserModel).filter_by(id=_id).delete()   #to delete the user based on id
        db.session.commit()     #commiting the changes back to database
        return {
            'Success' : 'User Deletion Success!!'
        },200       #return success message after deleting the user