import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from entity.customer import Customer
from entity.vehicle import Vehicle
from dao.imp.authenticationService import AuthenticationService
from dao.imp.customerService import CustomerService
from dao.imp.vehicleService import VehicleService

class TestMain(unittest.TestCase):

    def test_customer_authentication_invalid():
        auth_service = AuthenticationService()
        assert auth_service.authenticate_customer("anish123", "pass123")

    def test_update_customer_info(self):  
        customer_service = CustomerService()
        customer_data = Customer(
            customer_id= 1,
            first_name= " Name",
            last_name= " Name",
            email= "mail@gmail.com",
            phone_number= "1234567890",
            address= " Address",
            username= "username",
            password= "password"
        )
        assert customer_service.update_customer(customer_data)

  
    def test_update_vehicle_details(self):  
        vehicle_service = VehicleService()
        vehicle_data = {"vehicle_id": 1, "model": "Updated Model", "make": "Updated Make", "year": 2023, "color": "Blue", "registration_number": "UPDATED123", "availability": True, "daily_rate": 60}
        vehicle = Vehicle(**vehicle_data)
        assert vehicle_service.update_vehicle(vehicle)


    def test_get_available_vehicles(self):  
        vehicle_service = VehicleService()
        available_vehicles = vehicle_service.get_available_vehicles()
        assert available_vehicles is not None


    def test_get_all_vehicles(self):  
        vehicle_service = VehicleService()
        all_vehicles = vehicle_service.get_all_vehicles()
        assert all_vehicles is not None

if __name__ == '__main__':
    unittest.main()
