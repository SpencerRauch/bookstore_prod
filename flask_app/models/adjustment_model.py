from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

"""
REASON CODES:
0 - physical inventory check
1 - damaged in warehouse
2 - damaged in transit
3 - customer return
4 - internal use 
"""

class Adjustment:
    reasons = {
            0:'physical inventory check',
            1:'damaged in warehouse',
            2:'damaged in transit',
            3:'customer return',
            4:'internal use'
        }
    
    def __init__(self,data) -> None:
        self.id = data['id']
        self.quantity = data['quantity']
        self.reason = data['reason']
        self.employee_id = data['employee_id']
        self.stock_item_id = data['stock_item_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO adjustments (quantity, reason, employee_id, stock_item_id)
            VALUES (%(adjustment)s, %(reason)s, %(employee_id)s, %(stock_item_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM adjustments WHERE adjustments.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    
    @staticmethod
    def valid_adjustment(data):
        is_valid = True
        if len(data['adjustment']) <1:
            flash("quantity required")
            is_valid = False
        else: 
            try:
                int(data['adjustment'])
            except ValueError:
                is_valid = False
                flash("stock level must be an integer")
        if len(data['reason']) <1:
            flash("reason required")
            is_valid = False
        return is_valid

