from datetime import datetime
import mysql.connector

from dao.imp.customerService import CustomerService
from dao.imp.vehicleService import VehicleService
from dao.interface.IReservationService import IReservationService
from exception.exceptions import ReservationException
from util.db_connection import DBConnection

class ReservationService(IReservationService):
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

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params) if params else cursor.execute(query)
        return cursor

    def get_reservation_by_id(self, reservation_id):
        try:
            cursor = self.execute_query("SELECT * FROM reservation WHERE reservationID = %s", (reservation_id,))
            reservation = cursor.fetchone()
            return reservation
        except mysql.connector.Error as e:
            print("Error getting reservation by id:", e)
            return None
        finally:
            self.close_connection(cursor)

    def get_reservations_by_customer_id(self, customer_id):
        try:
            cursor = self.execute_query("SELECT * FROM reservation WHERE customerID = %s", (customer_id,))
            reservations = cursor.fetchall()
            return reservations
        except mysql.connector.Error as e:
            print("Error getting reservations by customer id:", e)
            return []
        finally:
            self.close_connection(cursor)

    def create_reservation(self, reservation):
        try:
            if not self.does_customer_exist(reservation.customer_id):
                raise ReservationException(f"Customer with ID {reservation.customer_id} does not exist.")
            if not self.does_vehicle_exist(reservation.vehicle_id):
                raise ReservationException(f"Vehicle with ID {reservation.vehicle_id} does not exist.")
            if self.is_vehicle_booked(reservation.vehicle_id, reservation.start_date, reservation.end_date, reservation_id=None):
                raise ReservationException("Vehicle is already booked for the specified dates.")

            cursor = self.execute_query("INSERT INTO reservation (customerID, vehicleID, startDate, endDate, totalCost, status) VALUES (%s, %s, %s, %s, %s, %s)",
                           (reservation.customer_id, reservation.vehicle_id, reservation.start_date, reservation.end_date, reservation.total_cost, reservation.status))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print("Error creating reservation:", e)
            return False
        except ReservationException as e:
            print("Reservation error:", e)
            return False
        finally:
            self.close_connection(cursor)

    def is_vehicle_booked(self, vehicle_id, start_date, end_date, reservation_id):
        try:
            cursor = self.execute_query("SELECT COUNT(*) FROM reservation WHERE vehicleID = %s AND ((%s BETWEEN startDate AND endDate) OR (%s BETWEEN startDate AND endDate))",
                        (vehicle_id, start_date, end_date)) if reservation_id is None else \
                     self.execute_query("SELECT COUNT(*) FROM reservation WHERE vehicleID = %s AND ((%s BETWEEN startDate AND endDate) OR (%s BETWEEN startDate AND endDate)) AND reservationID != %s",
                        (vehicle_id, start_date, end_date, reservation_id))
            count = cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as e:
            print("Error checking existing reservation:", e)
            return False
        finally:
            self.close_connection(cursor)

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
                raise ReservationException(message=f"Reservation with ID {reservation.reservation_id} not found.")
            if self.is_vehicle_booked(reser[2], reservation.start_date, reservation.end_date, reservation_id=reservation.reservation_id):
                raise ReservationException("Vehicle is already booked for the specified dates.")
            cursor = self.execute_query("UPDATE reservation SET customerID = %s, vehicleID = %s, startDate = %s, endDate = %s, totalCost = %s, status = %s WHERE reservationID = %s",
                           (reser[1], reser[2], reservation.start_date, reservation.end_date, reservation.total_cost, reservation.status, reservation.reservation_id))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print("Error updating reservation:", e)
            return False
        except ReservationException as e:
            print(e)
            return False
        finally:
            self.close_connection(cursor)

    def cancel_reservation(self, reservation_id):
        try:
            reser = self.get_reservation_by_id(reservation_id)
            if not reser:
                raise ReservationException(message=f"Reservation with ID {reservation_id} not found.")
            cursor = self.execute_query("DELETE FROM reservation WHERE reservationID = %s", (reservation_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print("Error canceling reservation:", e)
            return False
        except ReservationException as e:
            print(e)
            return False
        finally:
            self.close_connection(cursor)
