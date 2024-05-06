import csv
import random
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()

# For generating student information
class StudentProvider(BaseProvider):
    
    def studentalia(self, index):
        gender = self.random_element(["F", "M"])
        student_id = str(index + 1).zfill(6)  # Convert index position to 6-digit format
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (student_id, first_name, last_name, email_address, user_name)

# For generating lecturer information
class LecturerProvider(BaseProvider):
    
    def lectureralia(self, index):
        gender = self.random_element(["F", "M"])
        lecturer_id = str(index + 1).zfill(4)  # Convert index position to 4-digit format
        title = fake.prefix_male() if gender == "M" else fake.prefix_female()
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'user.myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (lecturer_id, title, first_name, last_name, email_address, user_name)

# For generating courses and course codes
Courses = ['MATH', 'SOCI', 'LING', 'BIO', 'CHEM', 'PHYS', 'MEDI', 'PSYCH', 'ECON', 'ACCT', 'POLI']
CourseN = ['Mathematics', 'Sociology', 'Linguistics', 'Biology', 'Chemistry', 'Physics', 'Medicine', 'Psychology', 'Economics', 'Accounting', 'Political Science']

CourseCode = []

# Repeat the process for each item in Courses
for course in Courses:
    # Repeat the process 20 times for each course
    for _ in range(20):
        # Generate a random integer between 1000 and 3501
        random_int = random.randint(1000, 3501)
        # Concatenate the course code with the random integer and append to CourseCode
        CourseCode.append(course + str(random_int))
        
# Create a dictionary where each item in CourseN is the key for every 20 items in CourseCode
ccdict = {course_name: CourseCode[i*20:(i+1)*20] for i, course_name in enumerate(CourseN)}

# For generating grades
class GradeProvider(BaseProvider):
    
    def grades(self):
        grades_data = {}
        for student_id, *_ in students:
            num_categories = random.randint(2, min(len(ccdict), 6))  # Select 2 to 6 categories randomly
            selected_categories = random.sample(CourseN, num_categories)
            selected_courses = [random.choice(ccdict[category]) for category in selected_categories]
            grades = [(course, random.randint(0, 100)) for course in selected_courses]
            grades_data[student_id] = grades
        return grades_data

fake.add_provider(StudentProvider)
fake.add_provider(LecturerProvider)
fake.add_provider(GradeProvider)

# Generate student and lecturer data
students = [fake.studentalia(index) for index in range(100000)]
lecturers = [fake.lectureralia(index) for index in range(55)]

# Generate grades data
grades_data = fake.grades()

# Flattening the grades data
grades_flat = [(student_id, course, grade) for student_id, grades in grades_data.items() for course, grade in grades]

try:
    # Writing student data to CSV
    with open('students.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student ID', 'First Name', 'Last Name', 'Email Address', 'User Name'])
        writer.writerows(students)

    # Writing lecturer data to CSV
    with open('lecturers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Lecturer ID', 'Title', 'First Name', 'Last Name', 'Email Address', 'User Name'])
        writer.writerows(lecturers)

    # Writing grades data to CSV
    with open('grades.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student ID', 'Course', 'Grade'])
        writer.writerows(grades_flat)

    print("Data generated and written to CSV files: students.csv, lecturers.csv, and grades.csv")

except Exception as e:
    print(f"An error occurred: {e}")
