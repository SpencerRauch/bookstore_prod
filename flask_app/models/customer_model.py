from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask_app.models import address_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class Customer:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.address_id = data['address_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address = address_model.Address.get_by_id({'id':self.address_id})


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO customers (name, address_id)
            VALUES (%(name)s, %(address_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = """ 
            UPDATE customers SET name = %(name)s WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM customers
            JOIN addresses ON address_id = addresses.id;
        """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_items = []
        for row in results:
            all_items.append(cls(row))
        return all_items
        
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM customers WHERE customers.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_name(cls,data):
        query = """
            SELECT * FROM customers WHERE customers.name = %(name)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def valid_customer(data):
        is_valid = True
        if len(data['name']) < 1:
            is_valid = False
            flash('Name required')
        return is_valid

