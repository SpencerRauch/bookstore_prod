from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask_app.models import purchase_line_item_model
from flask_app.models import manufacturer_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class PurchaseOrder:
    statuses = {
        0: 'entering',
        1: 'ordered',
        2: 'received',
        3: 'cancelled'
    }
    
    def __init__(self,data,with_items=False, with_manufacturer=False) -> None:
        self.id = data['id']
        self.status = data['status']
        self.employee_id = data['employee_id']
        self.manufacturer_id = data['manufacturer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if with_manufacturer:
            self.manufacturer = manufacturer_model.Manufacturer.get_by_id({'id':self.manufacturer_id})
        if with_items:
            self.items = purchase_line_item_model.PurchaseLineItem.get_all_for_order({'id':self.id})




    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO purchase_orders (employee_id, manufacturer_id)
            VALUES (%(employee_id)s, %(manufacturer_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def update_status(cls,data):
        query = """ 
            UPDATE purchase_orders SET status = %(status)s WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all_with_manufacturer(cls):
        query = """
            SELECT purchase_orders.*, manufacturers.*, COUNT(purchase_line_items.id) as item_count FROM purchase_orders
            JOIN manufacturers
            ON manufacturer_id = manufacturers.id
            LEFT JOIN purchase_line_items
            ON purchase_line_items.purchase_order_id = purchase_orders.id
            GROUP BY purchase_orders.id
            ORDER BY purchase_orders.id DESC;
        """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_items = []
        for row in results:
            one_order = cls(row)
            manu_data = {
                **row,
                'id': row['manufacturers.id'],
                'created_at':row['manufacturers.created_at'],
                'updated_at':row['manufacturers.updated_at']
            }
            one_order.manufacturer = manufacturer_model.Manufacturer(manu_data)
            one_order.item_count = row['item_count']
            all_items.append(one_order)
        return all_items
        
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM purchase_orders WHERE purchase_orders.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0], True, True)
        return False
    
    
    @staticmethod
    def valid_sale_order(data):
        is_valid = True
        if len(data['manufacturer_id']) < 1:
            is_valid = False
            flash('Manufacturer required')
        # potential_sale_order = Manufacturer.get_by_name({'name':data['name']})
        # if potential_sale_order:
        #     is_valid = False
        #     flash('Manufacturer exists by that name')
        return is_valid

