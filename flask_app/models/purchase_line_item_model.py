from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask_app.models import stockitem_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class PurchaseLineItem:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.ordered_quantity = data['ordered_quantity']
        self.received_quantity = data['received_quantity']
        self.stock_item_id = data['stock_item_id']
        self.purchase_order_id = data['purchase_order_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO purchase_line_items (ordered_quantity, purchase_order_id, stock_item_id)
            VALUES (%(ordered_quantity)s, %(purchase_order_id)s, %(stock_item_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def update_ordered(cls,data):
        query = """ 
            UPDATE purchase_line_items SET ordered_quantity = %(ordered_quantity)s WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)

    @classmethod
    def update_received(cls,data):
        query = """ 
            UPDATE purchase_line_items SET received_quantity = %(received_quantity)s WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def receive_full(cls, lines):
        for line in lines:
            if line.ordered_quantity == line.received_quantity:
                pass
            else:
                cls.update_received({"id":line.id,"received_quantity":line.ordered_quantity})
        
    
    @classmethod
    def get_on_hand_by_line(cls,data):
        query = """
            SELECT stock_level FROM purchase_line_items
            JOIN stock_items ON
            stock_items.id = stock_item_id
            WHERE purchase_line_items.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return results[0]['stock_level']
        return False
    
    @classmethod
    def delete(cls,data):
        query = """
            DELETE FROM purchase_line_items WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)

    @classmethod
    def get_all_for_order(cls, data):
        query = """
            SELECT * FROM purchase_line_items
            JOIN stock_items
            ON stock_items.id = stock_item_id
            WHERE purchase_order_id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        all_items = []
        for row in results:
            one_item = cls(row)
            one_item.stock_item = row['name']
            one_item.on_hand = row['stock_level']
            all_items.append(one_item)
        return all_items
        
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM purchase_line_items WHERE purchase_line_items.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    
    @staticmethod
    def valid_sale_line_item(data):
        is_valid = True
        if len(data['ordered_quantity']) < 1:
            is_valid = False
            flash('Quantity required','new_line')
        if len(data['stock_item_id']) < 1:
            is_valid = False
            flash('Item required','new_line')
        else:
            potential_stock_item = stockitem_model.StockItem.get_by_id({'id':data['stock_item_id']})
            if not potential_stock_item:
                is_valid = False
                flash('item not found','new_line')
        try:
            int_qty = int(data['ordered_quantity'])
            if int_qty < 0:
                flash("quantity must be positive",'new_line')
                is_valid = False
        except ValueError:
            flash("quantity should be numerical and positive",'new_line')
            is_valid = False
        return is_valid

