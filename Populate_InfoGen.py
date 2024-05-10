import csv
import mysql.connector

def insert_data_from_csv(cursor, filename, tablename, columns):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            values = [row.get(col, None) for col in columns]
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {tablename} ({', '.join(columns)}) VALUES ({placeholders})"
            try:
                cursor.execute(query, values)
            except mysql.connector.Error as err:
                print(f"Error inserting data into {tablename}: {err}")

try:
    # Connect to MySQL database
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="TrissSQL9845",
        database="School_System"
    )
    cursor = db.cursor()

    # Create Tables
    create_queries = [
        "CREATE TABLE IF NOT EXISTS Student (StudentID int PRIMARY KEY, UserID int, StudentName varchar(255), StudentEmail varchar(255), UserName varchar(255), FOREIGN KEY (UserID) REFERENCES Account(UserID))",
        "CREATE TABLE IF NOT EXISTS Lecturer (LecturerID int PRIMARY KEY, UserID int, LecturerName varchar(255), LecturerEmail varchar(255), UserName varchar(255), Department varchar(255), FOREIGN KEY (UserID) REFERENCES Account(UserID))",
        "CREATE TABLE IF NOT EXISTS Course (CourseCode varchar(255) PRIMARY KEY, CourseName varchar(255), Department varchar(255), StartDate date, EndDate date)",
        "CREATE TABLE IF NOT EXISTS Grades (StudentID int, CourseCode varchar(255), Grade int)",
        "CREATE TABLE IF NOT EXISTS Schedule (LecturerID int, CourseCode varchar(255), Department varchar(255))",
        "CREATE TABLE IF NOT EXISTS Account (UserID int PRIMARY KEY, UserName varchar(255), Password varchar(255))",
        "CREATE TABLE IF NOT EXISTS Admin (AdminID int PRIMARY KEY, UserID int, AdminName varchar(255), FOREIGN KEY (UserID) REFERENCES Account(UserID))"
    ]

    for query in create_queries:
        cursor.execute(query)

    # Insert data into tables
    insert_data_from_csv(cursor, 'students.csv', 'Student', ['StudentID', 'UserID', 'StudentName', 'StudentEmail', 'UserName'])
    insert_data_from_csv(cursor, 'lecturers.csv', 'Lecturer', ['LecturerID', 'UserID', 'LecturerName', 'LecturerEmail', 'UserName', 'Department'])
    insert_data_from_csv(cursor, 'courses.csv', 'Course', ['CourseCode', 'CourseName', 'Department', 'StartDate', 'EndDate'])
    insert_data_from_csv(cursor, 'grades.csv', 'Grades', ['StudentID', 'CourseCode', 'Grade'])
    insert_data_from_csv(cursor, 'lecturer_schedules.csv', 'Schedule', ['LecturerID', 'CourseCode', 'Department'])
    insert_data_from_csv(cursor, 'all_accounts.csv', 'Account', ['UserID', 'UserName', 'Password'])
    insert_data_from_csv(cursor, 'admins.csv', 'Admin', ['AdminID', 'UserID', 'AdminName'])

    # Commit changes
    db.commit()

except mysql.connector.Error as err:
    print("MySQL Error:", err)

finally:
    # Close database connection
    if cursor:
        cursor.close()
    if db:
        db.close()
