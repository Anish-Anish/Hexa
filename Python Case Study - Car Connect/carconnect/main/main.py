import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dao.imp.authenticationService import AuthenticationService
from dao.imp.reportsGenerator import ReportsGenerator
from exception.exceptions import AuthenticationException, InvalidInputException

from dao.imp.adminService import AdminService
from dao.imp.customerService import CustomerService
from dao.imp.reservationService import ReservationService
from dao.imp.vehicleService import VehicleService
from entity.admin import Admin
from entity.customer import Customer
from entity.reservation import Reservation
from entity.vehicle import Vehicle

class Menu:
    def __init__(self):
        self.customer_service = CustomerService()
        self.vehicle_service = VehicleService()
        self.reservation_service = ReservationService()
        self.admin_service = AdminService()
        self.authentication_service = AuthenticationService()
        self.reportsGenerator_service = ReportsGenerator()

    def format_datetime(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M")

    def display_menu(self):
        
        print("\n Car Connect: a Car Rental Platform")
        print("\n Menus:")
        print("1. Customer Operations")
        print("2. Vehicle Operations")
        print("3. Reservation Operations")
        print("4. Admin Operations")
        print("5. Authenticate Customer")
        print("6. Authenticate Admin")
        print("7. Generate Vehicles Report")
        print("8. Generate Reservations Report")
        print("9. Exit")
        
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.customer_operations()
            elif choice == '2':
                self.vehicle_operations()
            elif choice == '3':
                self.reservation_operations()
            elif choice == '4':
                self.admin_operations()
            elif choice == '5':
                self.authenticate_customer()
            elif choice == '6':
                self.authenticate_admin()
            elif choice == '7':
                self.generate_vehicle_report()
            elif choice == '8':
                self.generate_reservation_report()
            elif choice == '9':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def customer_operations(self):
        print("\nCustomer Operations:")
        print("1. Get customer by ID")
        print("2. Get customer by Username")
        print("3. Register customer")
        print("4. Update customer")
        print("5. Delete customer")

        choice = input("Enter your choice: ")

        if choice == '1':
            self.get_customer_by_id()
        elif choice == '2':
            self.get_customer_by_username()
        elif choice == '3':
            self.register_customer()
        elif choice == '4':
            self.update_customer()
        elif choice == '5':
            self.delete_customer()

    def get_customer_by_id(self):
        try:
            customer_id = int(input("Enter customer ID: "))
            customer = self.customer_service.get_customer_by_id(customer_id)
            if customer:
                print("Customer details:", customer)
        except ValueError:
            print("Invalid input for customer ID. Try giving the relevant information")

    def get_customer_by_username(self):
        username = input("Enter customer username: ")
        customer = self.customer_service.get_customer_by_username(username)
        if customer:
            print("Customer details:", customer)

    def register_customer(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        phone_number = input("Enter phone number: ")
        address = input("Enter address: ")
        username = input("Enter username: ")
        password = input("Enter password: ")

        customer_data = Customer(
            first_name= first_name,
            last_name= last_name,
            email= email,
            phone_number= phone_number,
            address= address,
            username= username,
            password= password,
        )
        success = self.customer_service.register_customer(customer_data)
        if success:
            print("Customer registered successfully.")
        else:
            print("Failed to register customer.")

    def update_customer(self):

        try:
            customer_id = int(input("Enter customer ID: "))
            first_name = input("Enter new first name: ")
            last_name = input("Enter new last name: ")
            email = input("Enter new email: ")
            phone_number = input("Enter new phone number: ")
            address = input("Enter new address: ")
            username = input("Enter new username: ")
            password = input("Enter new password: ")

            customer_data = Customer(
                customer_id= customer_id,
                first_name= first_name,
                last_name= last_name,
                email= email,
                phone_number= phone_number,
                address= address,
                username= username,
                password= password
            )
            success = self.customer_service.update_customer(customer_data)
            if success:
                print("Customer updated successfully.")
            else:
                print("Failed to update customer.")
        except InvalidInputException as e:
            print(e)
        except ValueError as e:
            print(e)

    def delete_customer(self):
        customer_id = int(input("Enter customer ID: "))

        success = self.customer_service.delete_customer(customer_id)
        if success:
            print("Customer deleted successfully.")
        else:
            print("Failed to delete customer.")


    def vehicle_operations(self):
        print("\nVehicle Operations:")
        print("1. Get vehicle by ID")
        print("2. Get available vehicles")
        print("3. Add vehicle")
        print("4. Update vehicle")
        print("5. Remove vehicle")

        choice = input("Enter your choice: ")

        if choice == '1':
            self.get_vehicle_by_id()
        elif choice == '2':
            self.get_available_vehicles()
        elif choice == '3':
            self.add_vehicle()
        elif choice == '4':
            self.update_vehicle()
        elif choice == '5':
            self.remove_vehicle()

    def get_vehicle_by_id(self):
        try:
            vehicle_id = int(input("Enter vehicle ID: "))
            vehicle = self.vehicle_service.get_vehicle_by_id(vehicle_id)
            if vehicle:
                print("Vehicle details:", vehicle)
        except ValueError:
            print("Invalid input for vehicle ID.  Try giving the relevant information")

    def get_available_vehicles(self):
        available_vehicles = self.vehicle_service.get_available_vehicles()
        if available_vehicles:
            print("Available vehicles:")
            for vehicle in available_vehicles:
                print(vehicle)
        else:
            print("No available vehicles.")

    def add_vehicle(self):
        model = input("Enter model: ")
        make = input("Enter make: ")
        year = int(input("Enter year: "))
        color = input("Enter color: ")
        registration_number = input("Enter registration number: ")
        availability = input("Is vehicle available? (yes-1/no-0): ")
        daily_rate = float(input("Enter daily rate: "))

        vehicle_data = Vehicle(
            model= model,
            make= make,
            year= year,
            color= color,
            registration_number= registration_number,
            availability= availability,
            daily_rate= daily_rate
        )
        success = self.vehicle_service.add_vehicle(vehicle_data)
        if success:
            print("Vehicle added successfully.")
        else:
            print("Failed to add vehicle.")

    def update_vehicle(self):
        vehicle_id = int(input("Enter vehicle ID: "))

        model = input("Enter new model: ")
        make = input("Enter new make: ")
        year = int(input("Enter new year: "))
        color = input("Enter new color: ")
        registration_number = input("Enter new registration number: ")
        availability = input("Is vehicle available? (no-0/yes-1): ")
        daily_rate = float(input("Enter new daily rate: "))

        vehicle_data = Vehicle(
            vehicle_id= vehicle_id,
            model= model,
            make= make,
            year= year,
            color= color,
            registration_number= registration_number,
            availability= availability,
            daily_rate= daily_rate
        )
        success = self.vehicle_service.update_vehicle(vehicle_data)
        if success == True:
            print("Vehicle updated successfully.")
        else:
            print("Failed to update vehicle.")

    def remove_vehicle(self):
        vehicle_id = int(input("Enter vehicle ID: "))

        success = self.vehicle_service.remove_vehicle(vehicle_id)
        if success:
            print("Vehicle removed successfully.")
        else:
            print("Failed to remove vehicle.")



    def reservation_operations(self):
        print("\nReservation Operations:")
        print("1. Get reservation by ID")
        print("2. Get reservations by Customer ID")
        print("3. Create reservation")
        print("4. Update reservation")
        print("5. Cancel reservation")

        choice = input("Enter your choice: ")

        if choice == '1':
            self.get_reservation_by_id()
        elif choice == '2':
            self.get_reservations_by_customer_id()
        elif choice == '3':
            self.create_reservation()
        elif choice == '4':
            self.update_reservation()
        elif choice == '5':
            self.cancel_reservation()

    def get_reservation_by_id(self):
        try:
            reservation_id = int(input("Enter reservation ID: "))
            reservation = self.reservation_service.get_reservation_by_id(reservation_id)
            if reservation:
                # Extracting reservation details
                res_id, user_id, room_id, start_time, end_time, amount, status = reservation
                # Formatting datetime objects
                start_time_formatted = self.format_datetime(start_time)
                end_time_formatted = self.format_datetime(end_time)
                # Printing reservation details without datetime objects
                print("Reservation details:")
                print("Reservation ID:", res_id)
                print("User ID:", user_id)
                print("Room ID:", room_id)
                print("Start Time:", start_time_formatted)
                print("End Time:", end_time_formatted)
                print("Amount:", amount)
                print("Status:", status)
            else:
                print(f"Reservation not found with id {reservation_id}.")
        except ValueError:
            print("Invalid input for reservation ID.")

    def get_reservations_by_customer_id(self):
        try:
            customer_id = int(input("Enter customer ID: "))
            reservations = self.reservation_service.get_reservations_by_customer_id(customer_id)
            if reservations:
                print("Reservations for customer ID", customer_id)
                for reservation in reservations:
                    res_id, user_id, room_id, start_time, end_time, amount, status = reservation

                    start_time_formatted = self.format_datetime(start_time)
                    end_time_formatted = self.format_datetime(end_time)

                    print("Reservation details:")
                    print("Reservation ID:", res_id)
                    print("User ID:", user_id)
                    print("Room ID:", room_id)
                    print("Start Time:", start_time_formatted)
                    print("End Time:", end_time_formatted)
                    print("Amount:", amount)
                    print("Status:", status)
                    print("\n")
            else:
                print("No reservations found for customer ID", customer_id)
        except ValueError:
            print("Invalid input for customer ID.")

    def create_reservation(self):
        customer_id = int(input("Enter customer ID: "))
        vehicle_id = int(input("Enter vehicle ID: "))
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        total_cost = float(input("Enter total cost: "))
        status = input("Enter status: ")

        reservation_data = Reservation(
            customer_id= customer_id,
            vehicle_id= vehicle_id,
            start_date= start_date,
            end_date= end_date,
            total_cost= total_cost,
            status= status
        )
        success = self.reservation_service.create_reservation(reservation_data)
        if success:
            print("Reservation created successfully.")
        else:
            print("Failed to create reservation.")

    def update_reservation(self):
        try:
            reservation_id = int(input("Enter reservation ID: "))

            start_date = input("Enter new start date (YYYY-MM-DD): ")
            end_date = input("Enter new end date (YYYY-MM-DD): ")
            total_cost = float(input("Enter new total cost: "))
            status = input("Enter new status: ")

            reservation_data = Reservation(
                reservation_id= reservation_id,
                start_date= start_date,
                end_date= end_date,
                total_cost= total_cost,
                status= status
            )
            success = self.reservation_service.update_reservation(reservation_data)
            if success:
                print("Reservation updated successfully.")
            else:
                print("Failed to update reservation.")
        except ValueError as e:
            print(e)
            return False

    def cancel_reservation(self):
        reservation_id = int(input("Enter reservation ID: "))

        success = self.reservation_service.cancel_reservation(reservation_id)
        if success:
            print("Reservation cancelled successfully.")
        else:
            print("Failed to cancel reservation.")


    def admin_operations(self):
        print("\nAdmin Operations:")
        print("1. Get admin by ID")
        print("2. Get admin by Username")
        print("3. Register admin")
        print("4. Update admin")
        print("5. Delete admin")

        choice = input("Enter your choice: ")

        if choice == '1':
            self.get_admin_by_id()
        elif choice == '2':
            self.get_admin_by_username()
        elif choice == '3':
            self.register_admin()
        elif choice == '4':
            self.update_admin()
        elif choice == '5':
            self.delete_admin()

    def get_admin_by_id(self):
        try:
            admin_id = int(input("Enter admin ID: "))
            admin = self.admin_service.get_admin_by_id(admin_id)
            if admin:
                print("Admin details:", admin)
        except ValueError:
            print("Invalid input for admin ID.")

    def get_admin_by_username(self):
        username = input("Enter admin username: ")
        admin = self.admin_service.get_admin_by_username(username)
        if admin:
            print("Admin details:", admin)

    def register_admin(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        phone_number = input("Enter phone number: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role: ")
        join_date = input("Enter join date (YYYY-MM-DD): ")

        admin_data = Admin(
            first_name= first_name,
            last_name= last_name,
            email= email,
            phone_number= phone_number,
            username= username,
            password= password,
            role= role,
            join_date= join_date
        )
        success = self.admin_service.register_admin(admin_data)
        if success:
            print("Admin registered successfully.")
        else:
            print("Failed to register admin.")

    def update_admin(self):
        admin_id = int(input("Enter admin ID: "))

        first_name = input("Enter new first name: ")
        last_name = input("Enter new last name: ")
        email = input("Enter new email: ")
        phone_number = input("Enter new phone number: ")
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        role = input("Enter new role: ")
        join_date = input("Enter new join date (YYYY-MM-DD): ")

        admin_data = Admin(
            admin_id= admin_id,
            first_name= first_name,
            last_name= last_name,
            email= email,
            phone_number= phone_number,
            username= username,
            password= password,
            role= role,
            join_date= join_date
        )
        success = self.admin_service.update_admin(admin_data)
        if success:
            print("Admin updated successfully.")
        else:
            print("Failed to update admin.")

    def delete_admin(self):
        admin_id = int(input("Enter admin ID: "))

        success = self.admin_service.delete_admin(admin_id)
        if success:
            print("Admin deleted successfully.")
        else:
            print("Failed to delete admin.")

    def authenticate_customer(self):
        username = input("Enter username: ")
        password = input("Enter password:")
        if self.authentication_service.authenticate_customer(username=username, password=password):
            print("Customer Authentication Successful.")
        
    def authenticate_admin(self):
        username = input("Enter username: ")
        password = input("Enter password:")
        if self.authentication_service.authenticate_admin(username=username, password=password):
            print("Admin Authentication Successful.")
        
    def generate_vehicle_report(self):
        self.reportsGenerator_service.generate_vehicle_report()

    def generate_reservation_report(self):
        self.reportsGenerator_service.generate_reservation_report()

if __name__ == "__main__":
    
    menu = Menu()
    menu.run()
