import mysql.connector
from util.db_connection import DBConnection
import mysql.connector
from util.db_connection import DBConnection

class ReportsGenerator:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if not self.connection:
            self.connection = DBConnection.getConnection()
        return self.connection

    def close_connection(self, cursor):
        if 'connection' in locals() and self.connection.is_connected():
            cursor.close()
            self.connection.close()

    def execute_query(self, query):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor

    def generate_vehicle_report(self):
        try:
            query = "SELECT COUNT(*) FROM vehicle WHERE availability = 1"
            cursor = self.execute_query(query)
            available_count = cursor.fetchone()[0]
            query = "SELECT COUNT(*) FROM vehicle"
            cursor = self.execute_query(query)
            total_count = cursor.fetchone()[0]
            availability_percentage = (available_count / total_count) * 100
            print("Vehicle Availability Analysis:")
            print(f"Total Vehicles: {total_count}")
            print(f"Available Vehicles: {available_count}")
            print(f"Availability Percentage: {availability_percentage:.2f}%")
        except mysql.connector.Error as e:
            print("Error generating vehicle report:", e)
        finally:
            self.close_connection(cursor)

    def generate_reservation_report(self):
        try:
            query = "SELECT status, COUNT(*) FROM reservation GROUP BY status"
            cursor = self.execute_query(query)
            reservation_statuses = cursor.fetchall()
            print("Reservation Status Analysis:")
            for status in reservation_statuses:
                print(f"Status: {status[0]}, Count: {status[1]}")
        except mysql.connector.Error as e:
            print("Error generating reservation report:", e)
        finally:
            self.close_connection(cursor)
