import mysql.connector

from dao.interface.IVehicleService import IVehicleService
from exception.exceptions import InvalidInputException, VehicleNotFoundException
from util.db_connection import DBConnection

class VehicleService(IVehicleService):
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

    def get_vehicle_by_id(self, vehicle_id):
        try:
            cursor = self.execute_query("SELECT * FROM vehicle WHERE vehicleID = %s", (vehicle_id,))
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
            self.close_connection(cursor)

    def get_all_vehicles(self):
        try:
            cursor = self.execute_query("SELECT * FROM vehicle")
            vehicles = cursor.fetchall()
            cursor.close()
            for veh in vehicles:
                print(veh)
            return vehicles
        except mysql.connector.Error as e:
            print("Error getting vehicle by id:", e)
            return None
        finally:
            self.close_connection(cursor)

    def get_available_vehicles(self):
        try:
            cursor = self.execute_query("SELECT * FROM vehicle WHERE availability = %s", (True,))
            vehicles = cursor.fetchall()
            cursor.close()
            return vehicles
        except mysql.connector.Error as e:
            print("Error getting available vehicles:", e)
            return []
        finally:
            self.close_connection(cursor)

    def add_vehicle(self, vehicle):
        try:
            cursor = self.execute_query("SELECT COUNT(*) FROM vehicle WHERE registrationNumber = %s", (vehicle.registration_number,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise InvalidInputException("A vehicle with the same registration number already exists")

            cursor = self.execute_query("INSERT INTO vehicle (model, make, year, color, registrationNumber, availability, dailyRate) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (vehicle.model, vehicle.make, vehicle.year, vehicle.color, vehicle.registration_number, vehicle.availability, vehicle.daily_rate))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print("Error adding vehicle:", e)
            return False
        except InvalidInputException as e:
            print(e)
            return False
        finally:
            self.close_connection(cursor)

    def update_vehicle(self, vehicle):
        try:
            veh = self.get_vehicle_by_id(vehicle.vehicle_id)
            if not veh:
                raise VehicleNotFoundException(message=f"Vehicle with ID {vehicle.vehicle_id} not found.")
            
            cursor = self.execute_query("SELECT vehicleID FROM vehicle WHERE registrationNumber = %s", (vehicle.registration_number,))
            existing_vehicle = cursor.fetchone()
            
            if existing_vehicle and existing_vehicle[0] != vehicle.vehicle_id:
                raise InvalidInputException("A vehicle with the same registration number already exists")
            
            cursor = self.execute_query("UPDATE vehicle SET model = %s, make = %s, year = %s, color = %s, registrationNumber = %s, availability = %s, dailyRate = %s WHERE vehicleID = %s",
                           (vehicle.model, vehicle.make, vehicle.year, vehicle.color, vehicle.registration_number, vehicle.availability, vehicle.daily_rate, vehicle.vehicle_id))
            self.connection.commit()
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
            self.close_connection(cursor)

    def remove_vehicle(self, vehicle_id):
        try:
            veh = self.get_vehicle_by_id(vehicle_id)
            if not veh:
                raise VehicleNotFoundException(message=f"Vehicle with ID {vehicle_id} not found.")
            
            cursor = self.execute_query("DELETE FROM vehicle WHERE vehicleID = %s", (vehicle_id,))
            self.connection.commit()
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
            self.close_connection(cursor)
