from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Employee:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.access_level = data['access_level']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO employees (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM employees WHERE employees.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False

    # @classmethod
    # def get_by_id_with_parties(cls,data):
    #     query = """
    #         SELECT * FROM employees LEFT JOIN parties ON employees.id = parties.employee_id WHERE employees.id = %(id)s;
    #     """
    #     results = connect_to_mysql(DATABASE).query_db(query,data)
    #     if results:
    #         employee_instance = cls(results[0])
    #         for row in results:
    #             if row['parties.id'] == None:
    #                 break
    #             party_data = {
    #                 **row,
    #                 'id':row['parties.id'],
    #                 'created_at':row['parties.created_at'],
    #                 'updated_at':row['parties.updated_at']
    #             }
    #             employee_instance.parties.append(party_model.Party(party_data))
    #         return employee_instance
    #     return False
    
    @classmethod
    def get_by_email(cls,data):
        query = """
            SELECT * FROM employees WHERE employees.email = %(email)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def valid_register(data):
        is_valid = True
        if len(data['first_name']) < 1:
            is_valid = False
            flash('First name required','reg')
        if len(data['last_name']) < 1:
            is_valid = False
            flash('Last name required','reg')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required','reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be in valid format','reg')
        elif not '@bookstore.com' in data['email']:
            is_valid = False
            flash('only bookstore.com emails allowed','reg')
        else:
            potential_employee = Employee.get_by_email({'email':data['email']})
            if potential_employee:
                is_valid = False
                flash('Email already registered, contact Admin','reg')
        if len(data['password']) < 1:
            is_valid = False
            flash("Please provide password", 'reg')
        elif len(data['password']) < 8:
            is_valid = False
            flash("Password must be > 8 char", 'reg')
        elif data['password'] != data['confirm_pass']:
            is_valid = False
            flash("Passwords do not match", 'reg')
        return is_valid

        