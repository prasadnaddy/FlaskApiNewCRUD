import sqlite3          #for the sqlite operations
from flask_restful import Resource      #for creating the API resources
import uuid         #module for generating unique User ID for the users while registration
from flask import request       #module for accepting the JSON request from API
from models.users import UserModel      #importing the user model from models
from db import db           #for sqlalchemy operations
from werkzeug.security import safe_str_cmp      #for comparing strings and make it work for all python versions
from flask_jwt_extended import (
    jwt_required,
    get_raw_jwt,
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity)   #for creating tokens and token refresh process
from blacklist import BLACKLIST         #for blacklisting the jwt tokens

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
        
class UserLogin(Resource):          #Resource for working with token login
    def post(self):
        try:
            body = request.get_json()           #fetching the username and password for token authentication from request
            user = UserModel.getUserByUserName(UserModel,body['username'])        #checking in db for the username 
            
            ##Checking if user exists and the passwords match or not here##
            if user and safe_str_cmp(user.password, body['password']):
                accessToken = create_access_token(identity=user.id, fresh=True)     #this is a fresh token
                refreshToken = create_refresh_token(identity=user.id)       #refresh token with user id as identity
                return {
                    'access_token' : accessToken,
                    'refresh_token' : refreshToken
                },200           #return the access and refresh token generated with 200 status code
            
            return {
                'Error' : 'User Not found, please provide correct credentials'
            },401           #user object is not valid
        except Exception as e:
            return {
                'Error' : 'Internal Server Error!!'
            },500       #internal server error gets caught up!
            
class UserRefreshToken(Resource):           #this is responsible for refreshing the token to get a new token
    @jwt_refresh_token_required             #refresh token provided with first access token is required for refreshing
    def post(self):     #POST method is used to send the refresh token as header
        try:
            currentUser = get_jwt_identity()        #getting the logged in user's identity value
            ##Now we will be creating access token with identity fetched from get_jwt_identity() function
            newToken = create_access_token(identity=currentUser, fresh=False)       #fresh is false for refresh token
            return {
                'access_token': newToken
            },200           #returning the new access token only with 200 status code
        except Exception as e:      #catching the exception and showing the error message on screen
            return {
                'Error' : 'Internal Server Error, please try again!!'
            },500
    
class UserLogout(Resource):             #this is responsible for logging out the users
    @jwt_required           #making sure that user must be logged in by passing the auth token
    def post(self):         #POST method to logout the users
        try:
            jti = get_raw_jwt()['jti']      #getting the JWT Token identity to blacklist it
            BLACKLIST.add(jti)      #adding the JWT token to blacklist set in another module
            return {
                'Message' : 'Thank you, You have been successfully Logged out!'
            },200
        except Exception as e:
            return {
                'Error' : 'Internal Server Error, please try after sometime'
            },500