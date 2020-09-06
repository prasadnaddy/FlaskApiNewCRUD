from flask import Flask, jsonify            #for creating the flask app
from flask_restful import Api     #for the restful apis and parsing requests
import secrets                  #module for generating the secret key
from flask_jwt_extended import JWTManager          #module for handling the authentication using extended module
from restfulsecurity import authenticate, identity     #security functions from another py file
from resources.userObject import (
    UserRegister, 
    User, 
    UserLogin, 
    UserRefreshToken,
    UserLogout
  )  #user register endpoint resource from user object class file
from resources.itemResources import Item, Items           #importing the resources from another file
from resources.storeResources import Store, Stores          #importing the store resources
from datetime import timedelta      #for adding up minutes or seconds to token expiration time
from models.items import ItemModel      #importing the items model, need to do it before calling db.create_all()
from models.users import UserModel      #importing the user model,  need to do it before calling db.create_all()
from models.store import StoreModel        #importing the store model, need to do it before db.create_all()
from flask_script import Manager, Server            #this will create some script files for DB upgrade / downgrade
from flask_migrate import Migrate, MigrateCommand           #for migrating the scripts created using upgrade/ downgrade
from db import db   #fetching the DB instance from db.py
import os           #for working with environment variables
from blacklist import BLACKLIST         #set containing the id of users to be blacklisted
    
app = Flask(__name__)       #creating the flask app
app.secret_key = secrets.token_hex(20)      #adding 20 bytes of secret key to app config
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)        #separate secret key for JWT Token
app.config['JWT_BLACKLIST_ENABLED'] = True      #enabling the blacklist behaviour
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']     #block both access and refresh tokens if sent for blacklisted user.
# app.config['JWT_AUTH_URL_RULE'] = '/token'      #changing the default endpoint to /token instead of /auth
# app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'      #changing the default prefix from JWT to Bearer
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=30)        #changing the default timeout
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///test.db') #setting DB URL, either heroku or sqlite
app.config['PROPAGATE_EXCEPTIONS'] = True       #to surpass the gunicorn JWT token error
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        #setting the track property to False

db.init_app(app)        #for creating the DB object for our app

@app.before_first_request           #this will affect all the functions below it, to execute before first request in flask
def createTables():
    db.create_all()         #sqlalchemy way of creating the tables if they dont exists
    
with app.app_context():     #creating the app context operations  
    if db.engine.url.drivername == 'sqlite':        #checking if our database is sqlite or not
        migrate = Migrate(app, db, render_as_batch=True)        #render as batch for altering columns in sqlite only
    else:
        migrate = Migrate(app, db)      #else go on as usual
    
##Creating the script manager to generate scripts for database migrations##
# manager = Manager(app)          #scripts manager object
# manager.add_command('db', MigrateCommand)           #adding the command to migrate the DB to our scripts manager

# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'     #this line deals with changing the default username key for identification
# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)       #creating the JWTManager object by passing our app

##JWT Claims means adding extra data to the JWT Payload##
@jwt.user_claims_loader     #adding the user related data as claims to the payload
def addClaimsData(identity):    #function to add the additional info
    if identity==1:     #making our first user as admin user, so taking his ID
        return {
            'isAdmin' : True        #if identity matches, then make him admin
        }
    return {
        'isAdmin' : False       #else, make the admin flag as false
    }

##Blacklisting the token behaviour is defined here##
@jwt.token_in_blacklist_loader      #if token is in blacklisted list, then this will work
def checkIfBlacklisted(decryptedToken):       #function that contains the behaviour for decrypted token
    return decryptedToken['jti'] in BLACKLIST      #return true if JWT Identity is blacklisted or else false

##JWT Custom messages to be shown when there are errors while accesing the JWT functionalities##
@jwt.expired_token_loader       #for changing the error message when access token is expired
def expiredTokenCallback():     #function to handle the expired token scenario
    return jsonify({
        'Description' : 'Sorry, Access token has expired.. Please generate a new one!',
        'Error_Code' : 'Token_Expired'
    }),401          #return the json form of the message when token is expired, this will overwrite the default one
    
@jwt.invalid_token_loader           #for changing the error message when invalid token is passed
def invalidTokenCallback(error):     #function to handle the invalid token scenario
    return jsonify({
        'Description' : 'Sorry, It is an invalid Token, please pass a valid token',
        'Error_Code' : 'Token_Invalid'
    }),401              #return the json form of the message when invalid token is passed to the header.
    
@jwt.unauthorized_loader            #for changing the error message when unauthorized header is sent
def unauthorizedHeaderCallback(error):
    return jsonify({
        'Description' : 'Sorry, Invalid Header.. please try with authorized header',
        'Error_Code' : 'Unauthorized_Header'
    }),401              #return the json form of the message when unauthorized header is passed
    
@jwt.needs_fresh_token_loader       #for changing the error message when fresh token is not passed when required
def freshTokenCallback():
    return jsonify({
        'Description' : 'Sorry, Fresh token is required.. Please pass a fresh token',
        'Error_Code' : 'Fresh_Token_Required'
    }),401              #return the json form of the message when fresh token is missing
    
@jwt.revoked_token_loader           #for changing the error message when revoked token is sent in header
def revokedTokenCallback():
    return jsonify({
        'Description' : 'Sorry, This token is revoked.. please generate a new one',
        'Error_Code' : 'Token_Revoked'
    }),401              #return the json form of the message when revoked token is passed

    
api = Api(app)      #for creating the api config from app

api.add_resource(Item,'/item/<string:name>')      #registering the Student Resource for API
api.add_resource(Items,'/items')      #registering the Items Resource for API
api.add_resource(UserRegister, '/register')     #for registering the users
api.add_resource(UserLogin, '/token')     #for fetching the access token
api.add_resource(UserLogout, '/logout')     #for logging out the users
api.add_resource(UserRefreshToken, '/refresh')     #for refreshing the token
api.add_resource(User, '/user/<int:_id>')     #for getting the users' information
api.add_resource(Store, '/store/<string:name>')     #for registering the users
api.add_resource(Stores, '/stores')     #for registering the users

if __name__=='__main__':        #make sure to run app only in main app.py file kind of file
    app.run()
    # manager.add_command('runserver',Server(port='1111', use_debugger=True)) #adding the params for port and debug mode
    # manager.run()           #this function is responsible for migrating the tables into the Database