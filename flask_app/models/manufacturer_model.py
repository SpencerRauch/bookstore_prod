from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class Manufacturer:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.address_id = data['address_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO manufacturers (name, address_id)
            VALUES (%(name)s, %(address_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM manufacturers WHERE manufacturers.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_name(cls,data):
        query = """
            SELECT * FROM manufacturers WHERE manufacturers.name = %(name)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def valid_manufacturer(data):
        is_valid = True
        potential_manufacturer = Manufacturer.get_by_name({'name':data['name']})
        if potential_manufacturer:
            is_valid = False
            flash('Manufacturer exists by that name')
        return is_valid

