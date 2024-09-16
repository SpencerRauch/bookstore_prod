from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask_app.models import sale_line_item_model
from flask_app.models import customer_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class SalesOrder:
    statuses = {
        0: 'entering',
        1: 'ordered',
        2: 'shipped',
        3: 'cancelled'
    }
    
    def __init__(self,data) -> None:
        self.id = data['id']
        self.status = data['status']
        self.employee_id = data['employee_id']
        self.customer_id = data['customer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO sale_orders (employee_id, customer_id)
            VALUES (%(employee_id)s, %(customer_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def update_status(cls,data):
        query = """ 
            UPDATE sale_orders SET status = %(status)s WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all_with_customer(cls):
        query = """
            SELECT * FROM sale_orders
            JOIN customers
            ON customer_id = customers.id;
        """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_items = []
        for row in results:
            one_order = cls(row)
            cust_data = {
                **row,
                'id': row['customers.id'],
                'created_at':row['customers.created_at'],
                'updated_at':row['customers.updated_at']
            }
            one_order.customer = customer_model.Customer(cust_data)
            all_items.append(one_order)
        return all_items
        
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM sale_orders WHERE sale_orders.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_name(cls,data):
        query = """
            SELECT * FROM sale_orders WHERE sale_orders.name = %(name)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def valid_sale_order(data):
        is_valid = True
        if len(data['name']) < 1:
            is_valid = False
            flash('Name required')
        # potential_sale_order = Manufacturer.get_by_name({'name':data['name']})
        # if potential_sale_order:
        #     is_valid = False
        #     flash('Manufacturer exists by that name')
        return is_valid
