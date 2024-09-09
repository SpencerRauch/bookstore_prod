from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class Address:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO addresses (street, city, state, zip)
            VALUES (%(street)s, %(city)s, %(state)s, %(zip)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM addresses WHERE addresses.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_name(cls,data):
        query = """
            SELECT * FROM addresses WHERE addresses.name = %(name)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def valid_address(data):
        is_valid = True
        if len(data['street']) <1:
            flash("Street required")
            is_valid = False
        if len(data['city']) <1:
            flash("City required")
            is_valid = False
        if len(data['state']) <1:
            flash("state required")
            is_valid = False
        if len(data['zip']) <1:
            flash("zip required")
            is_valid = False
        elif len(data['zip']) > 5:
            flash("please use 5 digit zip")
            is_valid = False
        return is_valid



