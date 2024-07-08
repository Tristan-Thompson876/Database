import pandas as pd
import mysql.connector
import time

# Read the CSV files into DataFrames
admins_df = pd.read_csv('admins.csv')
all_accounts_df = pd.read_csv('all_accounts.csv')
courses_df = pd.read_csv('courses.csv')
enrol_df = pd.read_csv('enrol.csv')
grades_df = pd.read_csv('grades.csv')
lecturer_schedules_df = pd.read_csv('lecturer_schedules.csv')
lecturers_df = pd.read_csv('lecturers.csv')
students_df = pd.read_csv('students.csv')

# Remove duplicate UserIDs in the Account DataFrame
#all_accounts_df = all_accounts_df.drop_duplicates(subset=['UserID'])

# Establish the database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='TrissSQL9845',
    database='School_System'
)

cursor = conn.cursor()

# Set the lock wait timeout
cursor.execute("SET innodb_lock_wait_timeout = 100;")

# Function to insert data into a table
## This function is not working as it should data is not being inserted in the table 
def insert_data(table_name, df, retries=3, delay=5):
    print("We are in insert data, I wonder if things will run smoothly")
    cols = ", ".join([str(i) for i in df.columns.tolist()])
    print(cols)
    print("Columns is above")
    for i, row in df.iterrows():
        print("iterating through df.iterrows")
        print(i)
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({'%s, ' * (len(row) - 1)}%s)"
        print("Should be inserted")
        for attempt in range(retries):
            try:
                cursor.execute(sql, tuple(row))
                print("Should execute sql scripts")
                break
            except mysql.connector.errors.IntegrityError as e:
                print(f"Error inserting into {table_name}: {e}")
                break
            except mysql.connector.errors.DatabaseError as e:
                if "Lock wait timeout exceeded" in str(e):
                    print(f"Lock wait timeout exceeded, retrying... (attempt {attempt + 1}/{retries})")
                    time.sleep(delay)
                else:
                    print(f"Database error inserting into {table_name}: {e}")
                    break
            except mysql.connector.errors.ProgrammingError as e:
                print(f"Programming error inserting into {table_name}: {e}")
                print(f"SQL: {sql}")
                print(f"Row data: {tuple(row)}")
                break
            except Exception as e:
                print(f"Unexpected error inserting into {table_name}: {e}")
                break

# Ensure the Grades table is created
create_grades_table_sql = """
CREATE TABLE IF NOT EXISTS Grades (
    StudentID INT,
    CourseCode VARCHAR(255),
    Grade DECIMAL(5,2),
    PRIMARY KEY (StudentID, CourseCode),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);
"""
cursor.execute(create_grades_table_sql)

# Insert data into the tables

print("Inserting into Account table")
insert_data('Account', all_accounts_df)
print("Inserting into Student table")
insert_data('Student', students_df)
print("Inserting into Admin table")
insert_data('Admin', admins_df)
print("Inserting into Lecturer table")
insert_data('Lecturer', lecturers_df)
print("Inserting into Course table")
insert_data('Course', courses_df)

# Insert data into the grades table with a check
valid_course_codes = set(courses_df['CourseCode'])

def insert_grades(df, valid_codes, retries=3, delay=5):
    cols = ", ".join([str(i) for i in df.columns.tolist()])
    print(i)
    print("[i] is above")
    for i, row in df.iterrows():
        if row['CourseCode'] in valid_codes:
            sql = f"INSERT INTO Grades ({cols}) VALUES ({'%s, ' * (len(row) - 1)}%s)"
            for attempt in range(retries):
                try:
                    cursor.execute(sql, tuple(row))
                    break
                except mysql.connector.errors.IntegrityError as e:
                    print(f"Error inserting into Grades: {e}")
                    break
                except mysql.connector.errors.DatabaseError as e:
                    if "Lock wait timeout exceeded" in str(e):
                        print(f"Lock wait timeout exceeded, retrying... (attempt {attempt + 1}/{retries})")
                        time.sleep(delay)
                    else:
                        print(f"Database error inserting into Grades: {e}")
                        break
                except mysql.connector.errors.ProgrammingError as e:
                    print(f"Programming error inserting into Grades: {e}")
                    print(f"SQL: {sql}")
                    print(f"Row data: {tuple(row)}")
                    break
                except Exception as e:
                    print(f"Unexpected error inserting into Grades: {e}")
                    break

print("Inserting into Grades table")
insert_grades(grades_df, valid_course_codes)

# Check and adjust DataFrame columns to match the table schema
#assignedcourse_columns = ['CourseID', 'LecturerID', 'Time', 'Room']  # Example column names, adjust as needed
#lecturer_schedules_df = lecturer_schedules_df[assignedcourse_columns]

# Continue with the rest of the tables
print("Inserting into Assignedcourse table")
insert_data('Assignedcourse', lecturer_schedules_df)
print("Inserting into Enrol table")
insert_data('Enrol', enrol_df)

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data has been successfully inserted into the database.")
