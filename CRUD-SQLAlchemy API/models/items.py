from db import db           #for importing sqlalchmey object
from models.store import StoreModel     #importing the store model

class ItemModel(db.Model):        #model for representing the Items
    __tablename__ = 'items'     #declaring the name of the table for sqlalchemy objects
    
    ##creating the columns for the table below##
    id = db.Column(db.Integer, primary_key=True)        #ID column is made as primary key
    name = db.Column(db.String(100))        #varchar column with 100 characters limit
    price = db.Column(db.String(15))           #varchar column for storing passwords
    type = db.Column(db.String(100))        #varchar column for storing the unique ID for users
    uniqueid = db.Column(db.String(50))     #for unique ID for users
    storename = db.Column(db.String(100), db.ForeignKey(StoreModel.name))       #foreign key mapping to stores id key column
    storeid = db.Column(db.Integer, db.ForeignKey(StoreModel.id))       #foreign key mapping to stores id key column
    store = db.relationship('StoreModel')       #creating relationship with Stores table by using relationship
    __table_args__ = (db.UniqueConstraint('storename', 'storeid',name='_stores_items_uc'),      #adding unique constraint for foreign key in postgressql
                 )
    def __init__(self, name, price, type, uniqueid, storename):
        super().__init__()
        self.name = name
        self.price = price
        self.type = type            #assigning the passed attributes for items into class variables
        self.uniqueid = uniqueid
        self.storename = storename
    
    def getItemByName(self,name):       #get item by passing the item name in the endpoint
        item = db.session.query(ItemModel).filter_by(name=name).first()      #getting the items based on name, first occurence
        if item:
            return item
        return 