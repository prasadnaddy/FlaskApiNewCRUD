from flask_restful import Resource, reqparse       #for creating the API and parsing request
from flask import request       #for handling the json request
from flask_jwt import jwt_required      #for the JWT Required condition
import uuid         #for generating the unique IDS
from models.items import ItemModel      #fetching the functions inside the item model from models
from db import db           #for sqlalchemy object

## We are creating API as resource with class and inherting the resource in every class
class Item(Resource):
    @jwt_required()      #decorator to indicate JWT token is necessary for getting this endpoint to work
    def get(self, name):
        try:
            item = ItemModel.getItemByName(ItemModel, name)
            if item:
                return {
                    'item': {
                        'name':item.name,
                        'price':item.price,
                        'type':item.type,
                    }
                    },200         #return the item json from get function with 200 status code
            return {
                'error':'Item not found in Database'
            },404
        except Exception as e:
            return {
                'Error' : 'Unexpected error occured at server side. Please try again'
            },500
        ##First lambda function to iterate over items list, and filter to find the matches,
        ##Next is used to iterate over the object given by filter, and calling it once finds first occurence.
        ##If item is not found, Next will throw exception, so we will be setting None, if not found
        # item = next(filter(lambda x: x['name']==name, items),None)
        ##If you dont like filters, you can use this below for loop instead of the filter line.
        # for item in items:      #iterating over the items list and checking if the name matches or not
        #     if item['name']==name:      #if matches, return the item json
        #         return {
        #             'item':item,         #returning the name sent for the GET method of this resource
        #         }
        # if item:
        #     return {
        #         'item': item,
        #     },200
        # return {
        #     'error':'The requested Item is not found'       #else, return error message with 404 error
        # },404
        
    def delete(self, name):
        try:
            item = ItemModel.getItemByName(ItemModel, name)     #get the item object
            if item:    # if item is found, then delete it
                db.session.query(ItemModel).filter_by(name=name).delete()   #to delete the item based on name
                db.session.commit()     #commiting the changes back to database
            # global items    #making global changes to the list
            # item = next(filter(lambda x: x['name']==name, items),None)  #first fetching the name if matches in our list
            # if item:        #if item is present, then only delete the item
            #     items = list(filter(lambda x: x['name']!=name, items))      #filter the items, not equal to name and ignore the one matching to delete it logically
                return {
                    'success':'Item with name {} has been deleted successfully!'.format(name)
                },200
            return {
                'error': 'The item is not found!'       #else, return the 404 error, item is not found
            },404
        except:
            return {
                'Error' : 'Unexpected error occured at server side. Please try again'
            },500
        
    def put(self,name):
        ## We can even add reqparse to make sure that payload can be accepted in a unique way like this
        # parser = reqparse.RequestParser()       #for passing the request sent for API
        # parser.add_argument(
        #     'price',required=True,help='Pass a price value'
        # )
        # body = parser.parse_args()
        try:
            body = request.get_json()       #getting the request as JSON
            try:
                if body['name']=='' or body['type']=='' or body['price']=='' or body['storename']=='' or not body:   #checking all fields
                    return {
                    'error':'Missing required fields to create the item, please fill name, type and price, storename params'
                },403           #returning error if fields are missed
            except KeyError:    #if any of the keys, got missed then we receive an exception, so handling it now
                return {
                    'error':'Missing required fields to create the item, please fill name, type and price, storename params'
                },403           #returning error if fields are missed
            item = ItemModel.getItemByName(ItemModel,body['name'])        #calling the getitemname function in Item class to get item object
            if item:        #if item is present, return error
                item.price = body['price']      #replace the price and types from body
                item.type = body['type']
                db.session.add(item)     #adding the user to our db
                db.session.commit()         #saving the changes
                return {
                    'Success' : 'Item with {} name has been updated successfully'.format(body['name'])
                },201
            else:
                uniqueID = str(uuid.uuid4())
                item = ItemModel(body['name'],body['price'],body['type'], uniqueID, body['storename'])
                db.session.add(item)     #adding the user to our db
                db.session.commit()         #saving the changes
                return {
                    'Success' : 'Item with {} name has been added to database with unique ID: {}'.format(body['name'], uniqueID)
                },201
        except Exception as e:
            return {
                    'Error':'Internal Server Error, Please try again'
                },201
            
class Items(Resource):
    def get(self):
        try:
            ##List comprehension to get all the items as JSON format##
            items = [{'name': row.name, 'price':row.price, 'type':row.type} for row in db.session.query(ItemModel).all()] #list comprehension to form a JSON list
            return {
                'items': items,         #returning the complete list of items as JSON response
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
                if body['name']=='' or body['type']=='' or body['price']=='' or body['storename']== '' or not body:   #checking all fields
                    return {
                    'error':'Missing required fields to create the item, please fill name, type and price, storename params'
                },403           #returning error if fields are missed
            except KeyError:    #if any of the keys, got missed then we receive an exception, so handling it now
                return {
                    'error':'Missing required fields to create the item, please fill name, type and price, storename params'
                },403           #returning error if fields are missed
            item = ItemModel.getItemByName(ItemModel,body['name'])        #calling the getitemname function in Item class to get item object
            if item:        #if item is present, return error
                return {
                    'Error' : 'This item already exists'
                },403
            uniqueID = str(uuid.uuid4())
            item = ItemModel(body['name'],body['price'],body['type'], uniqueID, body['storename'])
            db.session.add(item)     #adding the user to our db
            db.session.commit()         #saving the changes
            return {
                'Success' : 'Item with {} name has been added to database with unique ID: {}'.format(body['name'], uniqueID)
            },201
        except Exception as e:
            return {
                'Error' : 'Unexpected error occured at server side. Please try again'
            },500