from flask_restful import Resource          #for creating the resources for API
from models.store import StoreModel         #store model definition from models
from models.items import ItemModel
from db import db           #for sqlalchemy object
from flask import request           #for accepting requests from JSON
import uuid         #for generating uuid for stores

class Stores(Resource):
    def get(self):
        try:
            ##List comprehension to get all the stores as JSON format##
            stores = [{'name': row.name, 
                       'type':row.type, 
                       'items': [{'name': item.name, 'price':item.price, 'type':item.type} for item in db.session.query(ItemModel).filter_by(storename=row.name)]
                       } for row in db.session.query(StoreModel).all()] #list comprehension to form a JSON list
            return {
                'stores': stores,         #returning the complete list of items as JSON response
            },200
        except Exception as e:
            print(str(e))
            return {
                'Error' : 'Unexpected error occured at server side. Please try again'
            },500
    
    def post(self):
        try:
            body = request.get_json()       #getting the request as JSON
            try:
                if body['name']=='' or body['type']=='' or not body:   #checking all fields
                    return {
                    'error':'Missing required fields to create the store, please fill name, type params'
                },403           #returning error if fields are missed
            except KeyError:    #if any of the keys, got missed then we receive an exception, so handling it now
                return {
                    'error':'Missing required fields to create the store, please fill name, type params'
                },403           #returning error if fields are missed
            store = StoreModel.getStoreByName(StoreModel,body['name'])        #calling the getitemname function in Item class to get item object
            if store:        #if item is present, return error
                return {
                    'Error' : 'This item already exists'
                },403
            uniqueID = str(uuid.uuid4())
            store = StoreModel(body['name'],body['type'], uniqueID)
            store.uniqueid = uniqueID
            db.session.add(store)     #adding the user to our db
            db.session.commit()         #saving the changes
            return {
                'Success' : 'Store with {} name has been added to database with unique ID: {}'.format(body['name'], uniqueID)
            },201
        except Exception as e:
            print(str(e))
            return {
                'Error' : 'Unexpected error occured at server side. Please try again'
            },500
    
    
class Store(Resource):
    def get(self,name):
        try:
            store = StoreModel.getStoreByName(StoreModel, name)
            if store:
                return {
                    'store': {
                        'name':store.name,
                        'type':store.type,
                        'items': [{'name': row.name, 'price':row.price, 'type':row.type} for row in db.session.query(ItemModel).filter_by(storename=store.name).all()]
                    }
                    },200         #return the item json from get function with 200 status code
            return {
                'error':'Store not found in Database'
            },404
        except Exception as e:
            return {
                'Error' : 'Unexpected error occured at server side. Please try again'
            },500
    
    def delete(self,name):
        try:
            store = StoreModel.getStoreByName(StoreModel, name)     #get the item object
            if store:    # if item is found, then delete it
                db.session.query(StoreModel).filter_by(name=name).delete()   #to delete the item based on name
                db.session.commit()     #commiting the changes back to database
                return {
                    'success':'Store with name {} has been deleted successfully!'.format(name)
                },200
            return {
                'error': 'The Store is not found!'       #else, return the 404 error, item is not found
            },404
        except:
            return {
                'Error' : 'Unexpected error occured at server side. Please try again'
            },500