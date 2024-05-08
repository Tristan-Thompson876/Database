import csv
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="Schooly"
)
cursor = db.cursor()

# Create database if not exists
cursor.execute(f"CREATE DATABASE IF NOT EXISTS Schooly")

# Switch to Schooly database
cursor.execute(f"USE Schooly")

######################################### STUDENT INFO ##################################################

# Read and parse the Students CSV file
with open('students.csv', 'r') as file:
    reader = csv.DictReader(file)
    rows = [row for row in reader]

# Create Students table
cursor.execute(f"CREATE TABLE IF NOT EXISTS Students (PRIMARY KEY StudentID int, StudentName varchar(255), Email varchar(255), UserName varchar(255))")

# Commit changes
db.commit()

# Generate SQL insert statements
sql_inserts_s = []
for row in rows:
    sql_inserts_s.append(f"INSERT INTO Students (StudentID, StudentName, Email, UserName) VALUES ({row['Student ID']}, '{row['Student Name']}', {row['Email Address']}, {row['User Name']});")

# Write SQL insert statements to a SQL file
with open('populate_student_table.sql', 'w') as sql_file:
    sql_file.write('\n'.join(sql_inserts_s))
    
################################## LECTURER INFO ##################################################
 
# Read and parse the Lecturers CSV file
with open('lecturers.csv', 'r') as file:
    reader = csv.DictReader(file)
    rows = [row for row in reader]

# Create Lecturers table
cursor.execute(f"CREATE TABLE IF NOT EXISTS Lecturers (PRIMARY KEY LecturerID int, LecturerName varchar(255), Email varchar(255), UserName varchar(255), Department varchar(255))")

# Commit changes
db.commit()

# Generate SQL insert statements
sql_inserts_l = []
for row in rows:
    sql_inserts_l.append(f"INSERT INTO Lecturers (LecturerID, LecturerName, Email, UserName, Department) VALUES ({row['Lecturer ID']}, '{row['Lecturer Name']}', {row['Email Address']}, {row['User Name']}, {row['Department']});")

# Write SQL insert statements to a SQL file
with open('populate_lecturer_table.sql', 'w') as sql_file:
    sql_file.write('\n'.join(sql_inserts_l))
    
    
################################################# COURSE INFO ###############################################

# Read and parse the Courses CSV file
with open('courses.csv', 'r') as file:
    reader = csv.DictReader(file)
    rows = [row for row in reader]

# Create Courses table
cursor.execute(f"CREATE TABLE IF NOT EXISTS Courses (PRIMARY KEY Course Code varchar(255), CourseName varchar(255), Department varchar(255))")

# Commit changes
db.commit()

# Generate SQL insert statements
sql_inserts_c = []
for row in rows:
    sql_inserts_c.append(f"INSERT INTO Courses (CourseCode, CourseName, Department) VALUES ({row['Course Code']}, '{row['Course Name']}', {row['Department']});")

# Write SQL insert statements to a SQL file
with open('populate_student_table.sql', 'w') as sql_file:
    sql_file.write('\n'.join(sql_inserts_c))
    
    
################################################ GRADE INFO ################################################################

# Read and parse the Grades CSV file
with open('courses.csv', 'r') as file:
    reader = csv.DictReader(file)
    rows = [row for row in reader]

# Create Grades table
cursor.execute(f"CREATE TABLE IF NOT EXISTS Grades (StudentID int, CourseCode varchar(255), Grade int)")

# Commit changes
db.commit()

# Generate SQL insert statements
sql_inserts_g = []
for row in rows:
    sql_inserts_g.append(f"INSERT INTO Grades (StudentID, CourseCode, Grade) VALUES ({row['Student ID']}, '{row['Course Code']}', {row['Grade']});")

# Write SQL insert statements to a SQL file
with open('populate_student_table.sql', 'w') as sql_file:
    sql_file.write('\n'.join(sql_inserts_g))
