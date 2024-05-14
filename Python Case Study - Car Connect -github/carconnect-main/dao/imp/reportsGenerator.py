import mysql.connector
from util.db_connection import DBConnection

class ReportsGenerator:
    def generate_vehicle_report(self):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()

            query = "SELECT COUNT(*) FROM vehicle WHERE availability = 1"
            cursor.execute(query)
            available_count = cursor.fetchone()[0]
            query = "SELECT COUNT(*) FROM vehicle"
            cursor.execute(query)
            total_count = cursor.fetchone()[0]
            availability_percentage = (available_count / total_count) * 100
            print("Vehicle Availability Analysis:")
            print(f"Total Vehicles: {total_count}")
            print(f"Available Vehicles: {available_count}")
            print(f"Availability Percentage: {availability_percentage:.2f}%")
        except mysql.connector.Error as e:
            print("Error generating vehicle report:", e)
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def generate_reservation_report(self):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            query = "SELECT status, COUNT(*) FROM reservation GROUP BY status"
            cursor.execute(query)
            reservation_statuses = cursor.fetchall()
            print("Reservation Status Analysis:")
            for status in reservation_statuses:
                print(f"Status: {status[0]}, Count: {status[1]}")
        except mysql.connector.Error as e:
            print("Error generating reservation report:", e)
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

