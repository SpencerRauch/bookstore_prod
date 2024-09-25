from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask_app.models import employee_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

"""
STATUSES: 0 - Denied 
          1 - Granted 
          2 - New Request

REQUESTED LEVELS:
          0 - Sales
          1 - Inventory
          2 - Admin

"""

class Authorization:
    def __init__(self,data,with_requester=False, with_responder=False) -> None:
        self.id = data['id']
        self.status = data['status']
        self.requested_level = data['requested_level']
        self.requesting_id = data['requesting_id']
        self.responding_id = data['responding_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if with_requester:
            self.requester = employee_model.Employee.get_by_id({'id':self.requesting_id})
        if with_responder:
            if self.responding_id:
                self.responder = employee_model.Employee.get_by_id({'id':self.responding_id})
                
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM authorizations;
        """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_requests = []
        for row in results:
            all_requests.append(cls(row))
        return all_requests

    @classmethod
    def get_new_with_requester(cls):
        query = """
            SELECT * FROM authorizations WHERE status = 2;
        """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_requests = []
        for row in results:
            all_requests.append(cls(row,with_requester=True))
        return all_requests

    @classmethod
    def get_old(cls):
        query = """
            SELECT * FROM authorizations WHERE status != 2;
        """
        results = connect_to_mysql(DATABASE).query_db(query)
        all_requests = []
        for row in results:
            all_requests.append(cls(row,True,True))
        return all_requests
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM authorizations WHERE id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO authorizations (requested_level, requesting_id)
            VALUES (%(requested_level)s, %(requesting_id)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def grant(cls,data):
        query = """
            UPDATE authorizations 
            SET 
            status = 1,
            responding_id = %(responding_id)s
            WHERE authorizations.id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)

    @classmethod
    def deny(cls,data):
        query = """
            UPDATE authorizations 
            SET 
            status = 0,
            responding_id = %(responding_id)s
            WHERE authorizations.id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    

    

        