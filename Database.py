import mysql.connector
from mysql.connector import Error

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'TrissSQL9845'
}

def create_database_and_tables():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to MySQL Server")

            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS School_System")
            cursor.close()
            connection.close()
            
            db_config['database'] = 'School_System'
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            with open('tables.sql', 'r') as file:
                sql_commands = file.read().split(';')
                for command in sql_commands:
                    if command.strip() != '':
                        cursor.execute(command)
            connection.commit()
            cursor.close()
            print("Tables created successfully")
            
    except Error as e:
        print(f"Error creating database and tables: {e}")

if __name__ == '__main__':
    create_database_and_tables()
