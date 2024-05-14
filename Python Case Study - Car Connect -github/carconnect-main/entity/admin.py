import re
from exception.database_exceptions import DatabaseConnectionException
from exception.vehicle_exceptions import VehicleNotFoundException
from exception.customer_exceptions import CustomerNotFoundException
from exception.admin_exceptions import AdminNotFoundException
from exception.input_exceptions import InvalidInputException
from exception.authentication_exception import AuthenticationException
from exception.reservation_exception import ReservationException
from exception.vehicle_exceptions import VehicleNotFoundException

class Admin:
    def __init__(self, admin_id=None, first_name=None, last_name=None, email=None, phone_number=None, username=None, password=None, role=None, join_date=None):
        self.__admin_id = admin_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = self.__validate_email(email)
        self.__phone_number = phone_number
        self.__username = username
        self.__password = password
        self.__role = role
        self.__join_date = join_date

    def __validate_email(self, email):
        if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            return email
        else:
            print("Invalid email address.")

    @property
    def admin_id(self):
        return self.__admin_id

    @admin_id.setter
    def admin_id(self, value):
        self.__admin_id = value

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str):
            self.__first_name = first_name
        else:
            raise InvalidInputException("First name must be a string.")

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str):
            self.__last_name = last_name
        else:
            raise InvalidInputException("Last name must be a string.")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = self.__validate_email(email)

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone):
        if isinstance(phone, str) and phone.isdigit():
            self.__phone_number = phone
        else:
            raise InvalidInputException("Phone number must be a string containing only digits.")

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        self.__role = value

    @property
    def join_date(self):
        return self.__join_date

    @join_date.setter
    def join_date(self, value):
        self.__join_date = value

    def authenticate(self, password):
        return self.__password == password
