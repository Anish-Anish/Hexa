import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1', 
            port=3306,          
            user='root',
            password="ani28790'", 
            database='pet_pals'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall() 
        connection.commit()
        print("Query executed successfully")
        return result  
    except Error as e:
        print(f"Error executing query: {e}")
if __name__ == "__main__":
    connection = connect_to_database()
    if connection:
        your_query = "SELECT * FROM Pets"
        result = execute_query(connection, your_query)
        if result:
            for row in result:
                print(row) 
