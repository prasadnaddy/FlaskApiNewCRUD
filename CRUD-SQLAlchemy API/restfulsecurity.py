from werkzeug.security import safe_str_cmp      #for comparing strings and make it work for all python versions
from models.users import UserModel      #importing the user model from models

def authenticate(username, password):
    ##Get the username from mapping dict or else assign None if not found
    user = UserModel.getUserByUserName(UserModel, username)     #calling the class method to get the username details
    if user and safe_str_cmp(user.password,password):      #if user name is found, and password is matched, return user
        return user

def identity(payload):      #payload is from token
    uniqueid = payload['identity']        #getting the identity from payload
    return UserModel.getUserByID(UserModel, uniqueid)       #return the userid from userid method in class or else None if not found