import csv
import random
import hashlib
from faker import Faker
from collections import defaultdict
from datetime import datetime

fake = Faker()

# Define course prefixes and department names
Courses = ['MATH', 'SOCI', 'LING', 'BIO', 'CHEM', 'PHYS', 'MEDI', 'PSYCH', 'ECON', 'ACCT']
CourseN = ['Mathematics', 'Sociology', 'Linguistics', 'Biology', 'Chemistry', 'Physics', 'Medicine', 'Psychology', 'Economics', 'Accounting']

# Generate unique course codes
CourseCode = []
for course in Courses:
    for _ in range(20):
        while True:
            random_int = random.randint(1000, 3501)
            code = course + str(random_int)
            if code not in CourseCode:
                CourseCode.append(code)
                break

ccdict = {course_name: CourseCode[i*20:(i+1)*20] for i, course_name in enumerate(CourseN)}

class StudentProvider:
    def studentalia(self, index):
        gender = random.choice(["F", "M"])
        user_id = str(index + 67000001).zfill(6)
        student_id = str(index + 8000001).zfill(6)
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        student_name = first_name + ' ' + last_name
        email_address = f"{first_name.lower()}{student_id}@gmail.com"
        user_name = f"{first_name}_{last_name}"
        return (student_id, user_id, student_name, email_address, user_name)

class LecturerProvider:
    def __init__(self):
        self.departments = defaultdict(list)
        for lecturer, department in zip(range(len(CourseN) * 20), CourseN * 20):
            self.departments[department].append(lecturer)
    
    def lectureralia(self, index):
        gender = random.choice(["F", "M"])
        lecturer_id = str(index + 1).zfill(4)
        user_id = str(index + 4001).zfill(4)
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        lecturer_name = first_name + ' ' + last_name
        email_address = f"{first_name.lower()}.{last_name.lower()}@user.myschooly.com"
        user_name = f"{first_name}_{last_name}"
        department = CourseN[index // 20]
        return (lecturer_id, user_id, lecturer_name, email_address, user_name, department)

class CourseProvider:
    def __init__(self):
        self.generated_course_names = []
        prefixes = ["Introduction to", "Advanced", "Fundamentals of", "Exploring", "Applied", "Principles of", "Theoretical", "Dynamic", "General", "Analysing", "Contemporary", "Emerging", "Experimental", "Critical", "Interdisciplinary", "Global", 
                    "Digital", "Ethical", "Social", "Cultural", "Environmental", "Technical", "Professional"]
        random.shuffle(prefixes)
        generated_courses_dict = {course: set() for course in CourseN}
        for course in CourseN:
            while len(generated_courses_dict[course]) < 20:
                prefix = random.choice(prefixes)
                generated_course = f"{prefix} {course}"
                if generated_course not in generated_courses_dict[course]:
                    generated_courses_dict[course].add(generated_course)
        self.generated_course_names = [course_name for course_names in generated_courses_dict.values() for course_name in course_names]

    def course_data(self):
        course_data = []
        for i in range(200):
            course_code = CourseCode[i]
            course_name = self.generated_course_names[i]
            department_name = CourseN[i // 20]
            if i % 2 == 0:
                start_date = datetime(2024, 9, 6)
                end_date = datetime(2024, 12, 18)
            else:
                start_date = datetime(2024, 1, 17)
                end_date = datetime(2024, 5, 4)
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")
            course_data.append((course_code, course_name, department_name, start_date_str, end_date_str))
        return course_data

course_provider = CourseProvider()
courses = course_provider.course_data()

class GradeProvider:
    def grades(self):
        grades_data = {}
        for student_id, *_ in students:
            num_categories = random.randint(3, min(len(ccdict), 6))
            selected_categories = random.sample(CourseN, num_categories)
            selected_courses = [random.choice(ccdict[category]) for category in selected_categories]
            grades = [(course, random.randint(0, 100)) for course in selected_courses]
            grades_data[student_id] = grades
        return grades_data

class LectScheduleProvider:
    def __init__(self):
        self.departments = defaultdict(list)
        for lecturer, department in zip(range(len(CourseN) * 20), CourseN * 20):
            self.departments[department].append(lecturer)

    def lect_schedule(self):
        lect_schedule_data = []
        for lecturer_id, _, _, _, _, department in lecturers:
            dept_course_codes = [course[0] for course in courses if course[2] == department]
            if not dept_course_codes:
                continue
            random.shuffle(dept_course_codes)
            num_courses = random.randint(1, min(5, len(dept_course_codes)))
            selected_courses = dept_course_codes[:num_courses]
            lecturer_schedule = [(lecturer_id, course_code, department) for course_code in selected_courses]
            lect_schedule_data.extend(lecturer_schedule)
        return lect_schedule_data

class AccountProvider:
    def generate_password(self, user_id, user_name):
        unique_string = f"{user_id}{user_name}"
        hashed = hashlib.md5(unique_string.encode()).hexdigest()
        password = hashed[:8]
        return password
    
    def account_credentials(self, user_id, user_name):
        password = self.generate_password(user_id, user_name)
        return user_id, user_name, password

class AdminProvider:
    def generate_admin_id(self, lecturer_id):
        admin_id = 95000 + lecturer_id
        return admin_id
    
    def admin_data(self, lecturer_accounts):
        admin_data = []
        for user_id, user_name, _ in lecturer_accounts:
            lecturer_id = int(user_id) - 4000
            admin_id = self.generate_admin_id(int(lecturer_id))
            admin_data.append((admin_id, user_id, user_name))
        return admin_data

# Initialize providers
student_provider = StudentProvider()
lecturer_provider = LecturerProvider()
grade_provider = GradeProvider()
lect_schedule_provider = LectScheduleProvider()
account_provider = AccountProvider()
admin_provider = AdminProvider()

# Generate data
students = [student_provider.studentalia(index) for index in range(100000)]
lecturers = [lecturer_provider.lectureralia(index) for index in range(200)]
grades_data = grade_provider.grades()
grades_flat = [(student_id, course, grade) for student_id, grades in grades_data.items() for course, grade in grades]
lecturer_schedules = lect_schedule_provider.lect_schedule()
student_accounts = [account_provider.account_credentials(student[1], student[4]) for student in students]
lecturer_accounts = [account_provider.account_credentials(lecturer[1], lecturer[4]) for lecturer in lecturers]
admin_data = admin_provider.admin_data(lecturer_accounts)
all_accounts = student_accounts + lecturer_accounts

# Enrolment data generation
def generate_enrolments(students, courses):
    enrolments = defaultdict(list)
    course_members = defaultdict(int)
    
    for student in students:
        student_id = student[0]
        num_courses = random.randint(3, 6)
        selected_courses = random.sample(courses, num_courses)
        
        for course in selected_courses:
            course_code = course[0]
            enrolments[student_id].append(course_code)
            course_members[course_code] += 1
            
    # Ensure each course has at least 10 students
    for course_code in course_members:
        while course_members[course_code] < 10:
            student = random.choice(students)
            student_id = student[0]
            if course_code not in enrolments[student_id] and len(enrolments[student_id]) < 6:
                enrolments[student_id].append(course_code)
                course_members[course_code] += 1
    
    return enrolments

enrolments = generate_enrolments(students, courses)
enrol_flat = [(course_code, student_id) for student_id, courses in enrolments.items() for course_code in courses]

# Write data to CSV
try:
    # Writing student data to CSV
    with open('students.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['StudentID', 'UserID', 'StudentName', 'StudentEmail', 'UserName'])
        writer.writerows(students)

    # Writing lecturer data to CSV
    with open('lecturers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LecturerID', 'UserID', 'LecturerName', 'LecturerEmail', 'UserName', 'Department'])
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
        
    # Writing enrolment data to CSV
    with open('enrol.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CourseCode', 'StudentID'])
        writer.writerows(enrol_flat)

    print("Data generated and written to CSV files: students.csv, lecturers.csv, grades.csv, courses.csv, lecturer_schedules.csv, all_accounts.csv, admins.csv, and enrol.csv")

except Exception as e:
    print(f"An error occurred: {e}")
