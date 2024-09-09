from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class StockItem:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.stock_level = data['stock_level']
        self.manufacturer_id = data['manufacturer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO stock_items (name, stock_level, manufacturer_id)
            VALUES (%(name)s, %(stock_level)s, %(manufacturer_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM stock_items WHERE stock_items.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_name(cls,data):
        query = """
            SELECT * FROM stock_items WHERE stock_items.name = %(name)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def valid_stock_item(data):
        is_valid = True
        potential_item = StockItem.get_by_name({'name':data['name']})
        if potential_item.manufacturer_id == data['manufacturer_id'] :
            is_valid = False
            flash('item by that name exists for manufacturer')
        if len(data['name']) <1:
            flash("name required")
            is_valid = False
        if len(data['stock_level']) <1:
            flash("stock_level required")
            is_valid = False

        if len(data['stock_level']) < 0:
            is_valid = False
            flash('stock level cannot be negative')
        return is_valid

