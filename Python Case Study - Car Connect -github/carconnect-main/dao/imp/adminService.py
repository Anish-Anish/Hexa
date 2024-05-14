import mysql.connector

from dao.interface.IAdminService import IAdminService
from exception.database_exceptions import DatabaseConnectionException
from exception.vehicle_exceptions import VehicleNotFoundException
from exception.customer_exceptions import CustomerNotFoundException
from exception.admin_exceptions import AdminNotFoundException
from exception.input_exceptions import InvalidInputException
from exception.authentication_exception import AuthenticationException
from exception.reservation_exception import ReservationException
from exception.vehicle_exceptions import VehicleNotFoundException

from util.db_connection import DBConnection

class AdminService(IAdminService):
    def helper(self):
        self.connection = DBConnection.getConnection()
        cursor = self.connection.cursor()
        return cursor
        
    def connect_with_db(self):
        connection = DBConnection.getConnection()
        cursor = connection.cursor()
        return cursor
    
    def raise_exception(self, e):
        print(e)
        return None

    def get_admin_by_id(self, admin_id):
        try:
            cursor = self.helper()
            cursor.execute("SELECT * FROM admin WHERE adminID = %s", (admin_id,))
            admin = cursor.fetchone()
            cursor.close()
            if not admin:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found.")
            return admin
        except AdminNotFoundException as e:
            self.raise_exception(e)

    def get_admin_by_username(self, username):
        try:
            cursor = self.helper()
            cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
            admin = cursor.fetchone()
            cursor.close()
            if not admin:
                raise AdminNotFoundException(f"Admin with username {username} not found.")
            return admin
        except AdminNotFoundException as e:
            self.raise_exception(e)

    def register_admin(self, admin):
        try:
            cursor = self.connect_with_db()
            cursor.execute("SELECT COUNT(*) FROM admin WHERE username = %s", (admin.username,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise InvalidInputException("Admin with that username already exists")
            cursor.execute("INSERT INTO admin (firstName, lastname, email, phoneNumber, username, password, role, joinDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (admin.first_name, admin.last_name, admin.email, admin.phone_number, admin.username, admin.password, admin.role, admin.join_date))
            self.connection.commit()
            cursor.close()
            return True
        except InvalidInputException as e:
            self.raise_exception(e)

    def update_admin(self, admin):
        try:
            adm = self.get_admin_by_id(admin.admin_id)
            if not adm:
                raise AdminNotFoundException(f"Admin with ID {admin.admin_id} not found")
            cursor = self.connect_with_db()
            cursor.execute("SELECT adminID FROM admin WHERE username = %s", (admin.username,))
            existing_admin = cursor.fetchone()
            
            if existing_admin and existing_admin[0] != admin.admin_id:
                raise InvalidInputException("Admin with that username already exists")
            cursor.execute("UPDATE admin SET firstname = %s, lastname = %s, email = %s, phoneNumber = %s, username = %s, password = %s, role = %s WHERE adminID = %s",
                           (admin.first_name, admin.last_name, admin.email, admin.phone_number, admin.username, admin.password, admin.role, admin.admin_id))
            self.connection.commit()
            cursor.close()
            return True
        except InvalidInputException as e:
            self.raise_exception(e)

    def delete_admin(self, admin_id):
        try:
            adm = self.get_admin_by_id(admin_id)
            if not adm:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found")
            cursor = self.connect_with_db()
            cursor.execute("DELETE FROM admin WHERE adminID = %s", (admin_id,))
            self.connection.commit()
            cursor.close()
            return True
        except AdminNotFoundException as e:
            self.raise_exception(e)
