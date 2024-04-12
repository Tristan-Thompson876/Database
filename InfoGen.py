import csv
import random
from faker import Faker
from faker.providers import BaseProvider


# For generating student information

class StudentProvider(BaseProvider):
    
    def studentalia(self,index):
        gender = self.random_element(["F", "M"])
        student_id = str(index + 1).zfill(6)  # Convert index position to 6-digit format
        first_name = self.generator.first_name_male() if gender == "M" else self.generator.first_name_female()
        last_name = self.generator.last_name()
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (student_id, first_name, last_name, email_address, user_name)
        
fake = Faker()
fake.add_provider(StudentProvider)

student = [fake.studentalia(index) for index in range(10)]

print(student) # generated list of student particulars


# For generating lecturer information

class LecturerProvider(BaseProvider):
    
    def lectureralia(self,index):
        gender = self.random_element(["F", "M"])
        lecturer_id = str(index + 1).zfill(4)  # Convert index position to 4-digit format
        title = self.generator.prefix_male() if gender == "M" else self.generator.prefix_female()
        first_name = self.generator.first_name_male() if gender == "M" else self.generator.first_name_female()
        last_name = self.generator.last_name()
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'user.myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (lecturer_id, title, first_name, last_name, email_address, user_name)
        
fake = Faker()
fake.add_provider(LecturerProvider)

lecturer = [fake.lectureralia(index) for index in range(55)]

print(lecturer) # generated list of lecturer particulars

# For generating courses and course codes

Courses = ['MATH', 'SOCI', 'LING', 'BIO', 'CHEM', 'PHYS', 'MEDI', 'PSYCH', 'ECON', 'ACCT', 'POLI']
CourseN = ['Mathematics', 'Sociology', 'Linguistics', 'Biology', 'Chemistry', 'Physics', 'Medicine', 'Psychology', 'Economics', 'Accounting', 'Political Science']
CourseCode = []

# Repeat the process for each item in Courses
for course in Courses:
    # Repeat the process 20 times for each course
    for _ in range(20):
        # Generate a random integer between 1000 and 6501
        random_int = random.randint(1000, 6501)
        # Concatenate the course code with the random integer and append to CourseCode
        CourseCode.append(course + str(random_int))

# Display the first few items in CourseCode to verify
print(CourseCode)

# Create a dictionary where each item in CourseN is the key for every 20 items in CourseCode
ccdict = {course_name: CourseCode[i*20:(i+1)*20] for i, course_name in enumerate(CourseN)}

# Display the dictionary
print(ccdict) # dictionary generating 200 courses with 10 different areas of study: 20 courses each from lvl 1 to lvl 6

class GradeProvider(BaseProvider):
    
    def grades(self):
        grades_data = {}
        for student_id, *_ in student:
            num_courses = random.randint(4, 6)
            selected_courses = random.sample((CourseCode), num_courses)
            grades = [(course, random.randint(0, 100)) for course in selected_courses]
            grades_data[student_id] = [(course, grade) for course, grade in grades]
        return grades_data

fake.add_provider(GradeProvider)

grades_data = fake.grades()
print(grades_data)

# Flattening the grades data
grades_flat = [grade for sublist in grades_data for grade in sublist]

try:

    # Writing student data to CSV
    with open('students.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['First Name', 'Last Name', 'Email Address', 'User Name', 'Courses'])
        writer.writerows(student)

    # Writing lecturer data to CSV
    with open('lecturers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'First Name', 'Last Name', 'Email Address', 'User Name'])
        writer.writerows(lecturer)

    # Writing grades data to CSV
    with open('grades.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student Id', 'Course Grade'])
        writer.writerows(grades_flat)

    print("Data generated and written to CSV files: students.csv, lecturers.csv, and grades.csv")

except Exception as e:
    print(f"An error occurred: {e}")
