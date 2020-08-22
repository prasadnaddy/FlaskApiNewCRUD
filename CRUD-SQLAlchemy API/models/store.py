from db import db           #for creating the sqlalchemy object

class StoreModel(db.Model):
    __tablename__ = 'stores'     #declaring the name of the table for sqlalchemy objects
    
    ##creating the columns for the table below##
    id = db.Column(db.Integer, primary_key=True)        #ID column is made as primary key
    name = db.Column(db.String(100))        #varchar column with 100 characters limit
    type = db.Column(db.String(100))           #varchar column for storing passwords
    uniqueid = db.Column(db.String(100))        #varchar column for storing the unique ID for users
    items = db.relationship('ItemModel', lazy='dynamic')        #creating the relationship with ItemsModel as backreference
    
    ##[item.json() for item in self.items.all()]    to get the list of items for a store
    
    def __init__(self, name, type,uniqueID):
        super().__init__()
        # self.id = _id       #Using underscore as id is the predefined keyword
        self.name = name
        self.type = type
        self.uniqueid = uniqueID
        
    def getStoreByName(self,name):       #get item by passing the item name in the endpoint
        store = db.session.query(StoreModel).filter_by(name=name).first()      #getting the items based on name, first occurence
        if store:
            return store
        return 