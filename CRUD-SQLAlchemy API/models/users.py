from db import db           #for creating the sqlalchemy object

class UserModel(db.Model):
    __tablename__ = 'users'     #declaring the name of the table for sqlalchemy objects
    
    ##creating the columns for the table below##
    id = db.Column(db.Integer, primary_key=True)        #ID column is made as primary key
    username = db.Column(db.String(100))        #varchar column with 100 characters limit
    password = db.Column(db.String(100))           #varchar column for storing passwords
    uniqueid = db.Column(db.String(100))        #varchar column for storing the unique ID for users
    
    def __init__(self, username, password,uniqueID):
        super().__init__()
        # self.id = _id       #Using underscore as id is the predefined keyword
        self.username = username
        self.password = password
        self.uniqueID = uniqueID
        
    def getUserByUserName(self, username):
        user = db.session.query(UserModel).filter_by(username=username).first()     #select the user based on username
        if user:        #if present, return the user object
            return user
        return
        
    def getUserByID(self, _id):
        userid = db.session.query(UserModel).filter_by(id=_id).first()      #select the user based on ID
        if userid:      #if present return the user object
            return userid
        return