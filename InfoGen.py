import csv
import random
import hashlib
from faker import Faker
from faker.providers import BaseProvider
from collections import defaultdict
from datetime import datetime, timedelta

fake = Faker()

# For generating courses and course codes
Courses = ['MATH', 'SOCI', 'LING', 'BIO', 'CHEM', 'PHYS', 'MEDI', 'PSYCH', 'ECON', 'ACCT']
CourseN = ['Mathematics', 'Sociology', 'Linguistics', 'Biology', 'Chemistry', 'Physics', 'Medicine', 'Psychology', 'Economics', 'Accounting']

CourseCode = []  # Using a set to store unique course codes

# Repeat the process for each item in Courses.
for course in Courses:
    # Repeat the process 20 times for each course
    for _ in range(20):
        while True:
            # Generate a random integer between 1000 and 3501
            random_int = random.randint(1000, 3501)
            # Concatenate the course code with the random integer
            code = course + str(random_int)
            if code not in CourseCode:  # Check if code is unique
                CourseCode.append(code)  # Add unique code to the set
                break  # Break the loop if the code is unique
            # If code is not unique, regenerate it
        
# Create a dictionary where each item in CourseN is the key for every 20 items in CourseCode
ccdict = {course_name: CourseCode[i*20:(i+1)*20] for i, course_name in enumerate(CourseN)}

# For generating student information
class StudentProvider(BaseProvider):
    
    def studentalia(self, index):
        gender = self.random_element(["F", "M"])
        user_id = str(index + 67000001).zfill(6)
        student_id = str(index + 8000001).zfill(6)  # Adjusted to start from 8000001 and convert index position to 6-digit format
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        student_name = first_name + ' ' + last_name
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (student_id, user_id, student_name, email_address, user_name)

# For generating lecturer information
class LecturerProvider(BaseProvider):
    
    def __init__(self, generator):
        super().__init__(generator)
        self.departments = defaultdict(list)
        # Assign lecturers to departments
        for lecturer, department in zip(range(len(CourseN) * 20), CourseN * 20):
            self.departments[department].append(lecturer)
    
    def lectureralia(self, index):
        gender = self.random_element(["F", "M"])
        lecturer_id = str(index + 1).zfill(4)  # Convert index position to 4-digit format
        user_id = str(index + 4001).zfill(4)
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        lecturer_name = first_name + ' ' + last_name
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'user.myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        department = CourseN[index // 20]
        
        return (lecturer_id, user_id, lecturer_name, email_address, user_name, department)

# For generating course names
class CourseProvider(BaseProvider):
    
    def __init__(self, generator):
        super().__init__(generator)
        # List to store generated course names
        self.generated_course_names = []
        
        # Generate a shuffled list of prefixes
        prefixes = ["Introduction to", "Advanced", "Fundamentals of", "Exploring", "Applied", "Principles of", "Theoretical", "Dynamic", "General", "Analysing", "Contemporary", "Emerging", "Experimental", "Critical", "Interdisciplinary", "Global", 
                    "Digital", "Ethical", "Social", "Cultural", "Environmental", "Technical", "Professional"]
        random.shuffle(prefixes)

        # Dictionary to keep track of generated course names for each item
        generated_courses_dict = {course: set() for course in CourseN}

        # Repeat the process for each item in CourseN
        for course in CourseN:
            # Repeat until we have 20 unique course names for the current item
            while len(generated_courses_dict[course]) < 20:
                # Get a random prefix
                prefix = random.choice(prefixes)
                # Generate a course name
                generated_course = f"{prefix} {course}"
                # Add the generated course name to the set if it's not a duplicate
                if generated_course not in generated_courses_dict[course]:
                    generated_courses_dict[course].add(generated_course)

        # Flatten the dictionary values to get the list of generated course names
        self.generated_course_names = [course_name for course_names in generated_courses_dict.values() for course_name in course_names]

    def course_data(self):
        course_data = []
        for i in range(200):
            course_code = CourseCode[i]
            course_name = self.generated_course_names[i]
            department_name = CourseN[i // 20]
            # Determine start_date and end_date based on the condition
            if i % 2 == 0:
                start_date = datetime(2024, 9, 6)
                end_date = datetime(2024, 12, 18)
            else:
                start_date = datetime(2024, 1, 17)
                end_date = datetime(2024, 5, 4)
            
            # Format dates as strings without timestamps
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")
            
            course_data.append((course_code, course_name, department_name, start_date_str, end_date_str))
        return course_data

# Instantiate CourseProvider
course_provider = CourseProvider(fake)

# Generate course data
courses = course_provider.course_data()

# For generating grades
class GradeProvider(BaseProvider):
    
    def grades(self):
        grades_data = {}
        for student_id, *_ in students:
            num_categories = random.randint(3, min(len(ccdict), 6))  # Select 2 to 6 categories randomly
            selected_categories = random.sample(CourseN, num_categories)
            selected_courses = [random.choice(ccdict[category]) for category in selected_categories]
            grades = [(course, random.randint(0, 100)) for course in selected_courses]
            grades_data[student_id] = grades
        return grades_data
    
class LectScheduleProvider(BaseProvider):
    
    def __init__(self, generator):
        super().__init__(generator)
        self.departments = defaultdict(list)
        # Assign lecturers to departments
        for lecturer, department in zip(range(len(CourseN) * 20), CourseN * 20):
            self.departments[department].append(lecturer)

    def lect_schedule(self):
        lect_schedule_data = []
        for lecturer_id, _, _, _, _, department in lecturers:
            # Get all course codes for the lecturer's department
            dept_course_codes = [course[0] for course in courses if course[2] == department]
            if not dept_course_codes:
                continue  # Skip if no courses are available for the department
            # Shuffle the course codes
            random.shuffle(dept_course_codes)
            # Select a random number of distinct course codes between 1 and 5
            num_courses = random.randint(1, min(5, len(dept_course_codes)))
            # Select distinct course codes
            selected_courses = dept_course_codes[:num_courses]
            # Add lecturer ID and department to each selected course code
            lecturer_schedule = [(lecturer_id, course_code, department) for course_code in selected_courses]
            # Append to the schedule data
            lect_schedule_data.extend(lecturer_schedule)
        return lect_schedule_data
    
class AccountProvider(BaseProvider):
    
    def generate_password(self, user_id, user_name):
        # Concatenate user_id and user_name to create a unique string
        unique_string = f"{user_id}{user_name}"
        # Hash the unique string using MD5 algorithm
        hashed = hashlib.md5(unique_string.encode()).hexdigest()
        # Extract the first 8 characters of the hash as the password
        password = hashed[:8]
        return password
    
    def account_credentials(self, user_id, user_name):
        password = self.generate_password(user_id, user_name)
        return user_id, user_name, password
    
class AdminProvider(BaseProvider):
    
    def generate_admin_id(self, lecturer_id):
        # AdminID is generated by adding 95000 to LecturerID
        admin_id = 95000 + lecturer_id
        return admin_id
    
    def admin_data(self, lecturer_accounts):
        admin_data = []
        for user_id, user_name, _ in lecturer_accounts:
            # Extract lecturer ID from user_id
            lecturer_id = int(user_id) - 4000
            admin_id = self.generate_admin_id(int(lecturer_id))
            admin_data.append((admin_id, user_id, user_name))
        return admin_data


fake.add_provider(StudentProvider)
fake.add_provider(LecturerProvider)
fake.add_provider(GradeProvider)
fake.add_provider(CourseProvider)
fake.add_provider(AccountProvider)

# Generate student and lecturer data
students = [fake.studentalia(index) for index in range(100000)]
lecturers = [fake.lectureralia(index) for index in range(200)]

# Generate grades data
grades_data = fake.grades()

# Flattening the grades data
grades_flat = [(student_id, course, grade) for student_id, grades in grades_data.items() for course, grade in grades]

# Instantiate LectScheduleProvider
lect_schedule_provider = LectScheduleProvider(fake)

# Generate lecturer schedules
lecturer_schedules = lect_schedule_provider.lect_schedule()

# Generate account credentials for students
student_accounts = [fake.account_credentials(student[1], student[4]) for student in students]

# Generate account credentials for lecturers
lecturer_accounts = [fake.account_credentials(lecturer[1], lecturer[4]) for lecturer in lecturers]

# Generate admin data
admin_provider = AdminProvider(fake)
admin_data = admin_provider.admin_data(lecturer_accounts)

# Combine student_accounts and lecturer_accounts into all_accounts
all_accounts = student_accounts + lecturer_accounts


try:
    # Writing student data to CSV
    with open('students.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['StudentID', 'UserID', 'StudentName', 'Email', 'UserName'])
        writer.writerows(students)

    # Writing lecturer data to CSV
    with open('lecturers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LecturerID', 'UserID', 'LecturerName', 'Email', 'UserName', 'Department'])
        writer.writerows(lecturers)

    # Writing grades data to CSV
    with open('grades.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['StudentID', 'CourseCode', 'Grade'])
        writer.writerows(grades_flat)
        
    # Writing course data to CSV
    with open('courses.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CourseCode', 'CourseName', 'Department', 'StartDate', 'EndDate'])
        writer.writerows(courses)
        
    # Writing schedule data to CSV    
    with open('lecturer_schedules.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LecturerID', 'CourseCode', 'Department'])
        writer.writerows(lecturer_schedules)
        
    # Writing all accounts data to CSV
    with open('all_accounts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['UserID', 'UserName', 'Password'])
        writer.writerows(all_accounts)
        
    # Writing admin data to CSV
    with open('admins.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AdminID', 'UserID', 'AdminName'])
        writer.writerows(admin_data)

    print("Data generated and written to CSV files: students.csv, lecturers.csv, grades.csv, courses.csv, lecturer_schedules.csv, all_accounts.csv, and admins.csv")

except Exception as e:
    print(f"An error occurred: {e}")
