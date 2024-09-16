from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask_app.models import stockitem_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class SaleLineItem:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.ordered_quantity = data['ordered_quantity']
        self.shipped_quantity = data['shipped_quantity']
        self.stock_item_id = data['stock_item_id']
        self.sales_order_id = data['sales_order_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO sale_line_items (ordered_quantity, sales_order_id, stock_item_id)
            VALUES (%(ordered_quantity)s, %(sales_order_id)s, %(stock_item_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def update_ordered(cls,data):
        query = """ 
            UPDATE sale_line_items SET ordered_quantity = %(ordered_quantity)s WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)

    @classmethod
    def update_shipped(cls,data):
        query = """ 
            UPDATE sale_line_items SET shipped_quantity = %(shipped_quantity)s WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all_for_order(cls):
        query = """
            SELECT * FROM sale_line_items
            WHERE sales_order_id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_items = []
        for row in results:
            all_items.append(cls(row))
        return all_items
        
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM sale_line_items WHERE sale_line_items.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    
    @staticmethod
    def valid_sale_line_item(data):
        is_valid = True
        if len(data['quantity']) < 1:
            is_valid = False
            flash('Quantity required')
        if len(data['stock_item_id']) < 1:
            is_valid = False
            flash('Item required')
        potential_stock_item = stockitem_model.StockItem.get_by_id({'id':data['stock_item_id']})
        if not potential_stock_item:
            is_valid = False
            flash('item not found')
        try:
            int_qty = int(data['quantity'])
            if int_qty < 0:
                flash("quantiy must be positive")
                is_valid = False
        except ValueError:
            flash("quantity should be numerical and positive")
            is_valid = False
        return is_valid

