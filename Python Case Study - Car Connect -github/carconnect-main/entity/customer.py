import re
from exception.database_exceptions import DatabaseConnectionException
from exception.vehicle_exceptions import VehicleNotFoundException
from exception.customer_exceptions import CustomerNotFoundException
from exception.admin_exceptions import AdminNotFoundException
from exception.input_exceptions import InvalidInputException
from exception.authentication_exception import AuthenticationException
from exception.reservation_exception import ReservationException
from exception.vehicle_exceptions import VehicleNotFoundException
from datetime import datetime

class Customer:
    def __init__(self, customer_id=None, first_name="", last_name="", email="", phone_number="", address="", username="", password="", registration_date=None):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = self.__validate_email(email)
        self.__phone_number = phone_number
        self.__address = address
        self.__username = username
        self.__password = password
        self.__registration_date = datetime.now()

    def __validate_email(self, email):
        if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            return email
        else:
            raise InvalidInputException("Invalid email address provided.")

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = value

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
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        if isinstance(address, str):
            self.__address = address
        else:
            raise InvalidInputException("Address must be a string.")

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
    def registration_date(self):
        return self.__registration_date

    @registration_date.setter
    def registration_date(self, value):
        self.__registration_date = value

    def authenticate(self, password):
        return self.__password == password





