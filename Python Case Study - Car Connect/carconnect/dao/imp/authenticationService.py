from dao.imp.adminService import AdminService
from dao.imp.customerService import CustomerService
from exception.exceptions import AuthenticationException


class AuthenticationService:
    def __init__(self):
        self.cust_obj = CustomerService()
        self.admin_obj = AdminService()

    def authenticate_customer(self, username, password):
        try:
            customer = self.cust_obj.get_customer_by_username(username)
            if customer and customer[7] == password:
                return True
            else:
                raise AuthenticationException("Customer Authentication Unsuccessful.\n Incorrect username or password")
        except AuthenticationException as e:
            print(e)
            return False
        
    def authenticate_admin(self, username, password):
        try:
            admin = self.admin_obj.get_admin_by_username(username)
            if admin and admin[6] == password:
                return True
            else:
                raise AuthenticationException("Admin Authentication Unsuccessful.\n Incorrect username or password")
        except AuthenticationException as e:
            print(e)
            return False


