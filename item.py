import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This is field is required!')


    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"item": {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert_the_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update_the_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price =? WHERE name =?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        #     return {'message': "An item with the name '{}' already exist.".format(name)}, 400
        item = self.find_by_name(name)
        if item:
            return {'message': "An item with the name '{}' already exist.".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        Item.insert_the_item(item)
        return item, 201


    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name= ?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {'message': 'Item has been deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert_the_item(updated_item)
            except:
                return {"message": "An error occurred while entering the item"}, 500
        else:
            try:
                self.update_the_item(updated_item)
            except:
                return {"message": "An error occurred while updating the item"}, 500

        return updated_item

class Items(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {"items": items}