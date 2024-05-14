from datetime import datetime
import mysql.connector

from dao.imp.customerService import CustomerService
from dao.imp.vehicleService import VehicleService
from dao.interface.IReservationService import IReservationService
from exception.database_exceptions import DatabaseConnectionException
from exception.vehicle_exceptions import VehicleNotFoundException
from exception.customer_exceptions import CustomerNotFoundException
from exception.admin_exceptions import AdminNotFoundException
from exception.input_exceptions import InvalidInputException
from exception.authentication_exception import AuthenticationException
from exception.reservation_exception import ReservationException
from exception.vehicle_exceptions import VehicleNotFoundException

from util.db_connection import DBConnection

class ReservationService(IReservationService):
    def get_reservation_by_id(self, reservation_id):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM reservation WHERE reservationID = %s", (reservation_id,))
            reservation = cursor.fetchone()
            cursor.close()
            return reservation
        except mysql.connector.Error as e:
            print("Error getting reservation by id:", e)
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def get_reservations_by_customer_id(self, customer_id):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM reservation WHERE customerID = %s", (customer_id,))
            reservations = cursor.fetchall()
            cursor.close()
            return reservations
        except mysql.connector.Error as e:
            print("Error getting reservations by customer id:", e)
            return []
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def create_reservation(self, reservation):
        try:
            if not self.does_customer_exist(reservation.customer_id):
                raise ReservationException(f"Customer with ID {reservation.customer_id} does not exist.")
            if not self.does_vehicle_exist(reservation.vehicle_id):
                raise ReservationException(f"Vehicle with ID {reservation.vehicle_id} does not exist.")
            if self.is_vehicle_booked(reservation.vehicle_id, reservation.start_date, reservation.end_date, reservation_id=None):
                raise ReservationException("Vehicle is already booked for the specified dates.")

            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO reservation (customerID, vehicleID, startDate, endDate, totalCost, status) VALUES (%s, %s, %s, %s, %s, %s)",
                           (reservation.customer_id, reservation.vehicle_id, reservation.start_date, reservation.end_date, reservation.total_cost, reservation.status))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error creating reservation:", e)
            return False
        except ReservationException as e:
            print("Reservation error:", e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def is_vehicle_booked(self, vehicle_id, start_date, end_date, reservation_id):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if(reservation_id == None):
                cursor.execute("SELECT COUNT(*) FROM reservation WHERE vehicleID = %s AND ((%s BETWEEN startDate AND endDate) OR (%s BETWEEN startDate AND endDate))",
                        (vehicle_id, start_date, end_date))
            else:
                cursor.execute("SELECT COUNT(*) FROM reservation WHERE vehicleID = %s AND ((%s BETWEEN startDate AND endDate) OR (%s BETWEEN startDate AND endDate)) AND reservationID != %s",
                        (vehicle_id, start_date, end_date, reservation_id))
            count = cursor.fetchone()[0]
            return count>0
        except mysql.connector.Error as e:
            print("Error checking existing reservation:", e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def does_customer_exist(self, customer_id):
        customer_service = CustomerService()
        customer = customer_service.get_customer_by_id(customer_id)
        return customer is not None
    
    def does_vehicle_exist(self, vehicle_id):
        vehicle_service = VehicleService()
        vehicle = vehicle_service.get_vehicle_by_id(vehicle_id)
        return vehicle is not None


    def update_reservation(self, reservation):
        try:
            reser = self.get_reservation_by_id(reservation.reservation_id)
            if not reser:
                raise ReservationException(message=f"reservation with ID {reservation.reservation_id} not found.")
            if self.is_vehicle_booked(reser[2], reservation.start_date, reservation.end_date, reservation_id=reservation.reservation_id):
                raise ReservationException("Vehicle is already booked for the specified dates.")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("UPDATE reservation SET customerID = %s, vehicleID = %s, startDate = %s, endDate = %s, totalCost = %s, status = %s WHERE reservationID = %s",
                           (reser[1], reser[2], reservation.start_date, reservation.end_date, reservation.total_cost, reservation.status, reservation.reservation_id))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error updating reservation:", e)
            return False
        except ReservationException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def cancel_reservation(self, reservation_id):
        try:
            reser = self.get_reservation_by_id(reservation_id)
            if not reser:
                raise ReservationException(message=f"reservation with ID {reservation_id} not found.")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM reservation WHERE reservationID = %s", (reservation_id,))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error canceling reservation:", e)
            return False
        except ReservationException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
