
import mysql.connector
from exception.exceptions import DatabaseConnectionException

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
        
