
import mysql.connector
from exception.database_exceptions import DatabaseConnectionException
from exception.vehicle_exceptions import VehicleNotFoundException
from exception.customer_exceptions import CustomerNotFoundException
from exception.admin_exceptions import AdminNotFoundException
from exception.input_exceptions import InvalidInputException
from exception.authentication_exception import AuthenticationException
from exception.reservation_exception import ReservationException
from exception.vehicle_exceptions import VehicleNotFoundException


class DBConnection:
    __connection = None

    @staticmethod
    def getConnection():
        try:
            DBConnection.__connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ani28790'",
                database="carconnect2",
                port=3306
            )
            print("Connected to MySQL database successfully.")
            return DBConnection.__connection
        except mysql.connector.Error as err:
            print("Error connecting to MySQL:", err)
            raise DatabaseConnectionException(err)
        
