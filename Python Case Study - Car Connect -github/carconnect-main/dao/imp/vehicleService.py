import mysql.connector

from dao.interface.IVehicleService import IVehicleService
from exception.database_exceptions import DatabaseConnectionException
from exception.vehicle_exceptions import VehicleNotFoundException
from exception.customer_exceptions import CustomerNotFoundException
from exception.admin_exceptions import AdminNotFoundException
from exception.input_exceptions import InvalidInputException
from exception.authentication_exception import AuthenticationException
from exception.reservation_exception import ReservationException
from exception.vehicle_exceptions import VehicleNotFoundException

from util.db_connection import DBConnection

class VehicleService(IVehicleService):

    def get_vehicle_by_id(self, vehicle_id):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM vehicle WHERE vehicleID = %s", (vehicle_id,))
            vehicle = cursor.fetchone()
            cursor.close()
            if not vehicle:
                raise VehicleNotFoundException("Vehicle not found.")
            return vehicle
        except mysql.connector.Error as e:
            print("Error getting vehicle by id:", e)
            return None
        except VehicleNotFoundException as e:
            print(e)
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def get_all_vehicles(self):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM vehicle")
            vehicles = cursor.fetchall()
            cursor.close()
            for veh in vehicles:
                print(veh)
            return vehicles
        except mysql.connector.Error as e:
            print("Error getting vehicle by id:", e)
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def get_available_vehicles(self):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM vehicle WHERE availability = %s", (True,))
            vehicles = cursor.fetchall()
            cursor.close()
            return vehicles
        except mysql.connector.Error as e:
            print("Error getting available vehicles:", e)
            return []
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def add_vehicle(self, vehicle):
        try:
            connection = DBConnection.getConnection()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM vehicle WHERE registrationNumber = %s", (vehicle.registration_number,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise InvalidInputException("A vehicle with the same registration number already exists")

            cursor.execute("INSERT INTO vehicle (model, make, year, color, registrationNumber, availability, dailyRate) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (vehicle.model, vehicle.make, vehicle.year, vehicle.color, vehicle.registration_number, vehicle.availability, vehicle.daily_rate))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error adding vehicle:", e)
            return False
        except InvalidInputException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()


    def update_vehicle(self, vehicle):
        try:
            veh = self.get_vehicle_by_id(vehicle.vehicle_id)
            if not veh:
                raise VehicleNotFoundException(message=f"vehicle with {vehicle.vehicle_id} not found.")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("SELECT vehicleID FROM vehicle WHERE registrationNumber = %s", (vehicle.registration_number,))
            existing_vehicle = cursor.fetchone()
            
            if existing_vehicle and existing_vehicle[0] != vehicle.vehicle_id:
                raise InvalidInputException("A vehicle with the same registration number already exists")
            
            cursor.execute("UPDATE vehicle SET model = %s, make = %s, year = %s, color = %s, registrationNumber = %s, availability = %s, dailyRate = %s WHERE vehicleID = %s",
                           (vehicle.model, vehicle.make, vehicle.year, vehicle.color, vehicle.registration_number, vehicle.availability, vehicle.daily_rate, vehicle.vehicle_id))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print("Error updating vehicle:", e)
            return False
        except InvalidInputException as e:
            print(e)
            return False
        except VehicleNotFoundException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def remove_vehicle(self, vehicle_id):
        try:
            veh = self.get_vehicle_by_id(vehicle_id)
            if not veh:
                raise VehicleNotFoundException(message=f"vehicle with {vehicle_id} not found.")
            connection = DBConnection.getConnection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM vehicle WHERE vehicleID = %s", (vehicle_id,))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            if e.errno == 1451:
                print("Cannot delete vehicle. There are reservations associated with this vehicle.")
            else:
                print("Error removing vehicle:", e)
            return False
        except VehicleNotFoundException as e:
            print(e)
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
