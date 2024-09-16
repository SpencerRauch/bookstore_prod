from flask_app import app
from flask_app.controllers import employee_controller, authorizations_controller, inventory_controller, manufacturers_controller, sales_controller, customers_controller

if __name__=='__main__':
    app.run(debug=True)
