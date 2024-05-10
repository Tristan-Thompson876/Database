import csv
import random
from faker import Faker
from faker.providers import BaseProvider
from collections import defaultdict
from datetime import datetime, timedelta

fake = Faker()

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

# For generating student information
class StudentProvider(BaseProvider):
    
    def studentalia(self, index):
        gender = self.random_element(["F", "M"])
        student_id = str(index + 1).zfill(6)  # Convert index position to 6-digit format
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        student_name = first_name + ' ' + last_name
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (student_id, student_name, email_address, user_name)

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
        first_name = fake.first_name_male() if gender == "M" else fake.first_name_female()
        last_name = fake.last_name()
        lecturer_name = first_name + ' ' + last_name
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'user.myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        department = CourseN[index // 20]
        
        return (lecturer_id, lecturer_name, email_address, user_name, department)

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
        for lecturer_id, _, _, _, department in lecturers:
            # Get all course codes for the lecturer's department
            dept_course_codes = [course[0] for course in courses if course[2] == department]
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

fake.add_provider(StudentProvider)
fake.add_provider(LecturerProvider)
fake.add_provider(GradeProvider)
fake.add_provider(CourseProvider)

# Generate student and lecturer data
students = [fake.studentalia(index) for index in range(100)]
lecturers = [fake.lectureralia(index) for index in range(200)]

# Generate grades data
grades_data = fake.grades()

# Flattening the grades data
grades_flat = [(student_id, course, grade) for student_id, grades in grades_data.items() for course, grade in grades]

# Instantiate LectScheduleProvider
lect_schedule_provider = LectScheduleProvider(fake)

# Generate lecturer schedules
lecturer_schedules = lect_schedule_provider.lect_schedule()

try:
    # Writing student data to CSV
    with open('students.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student ID', 'Student Name', 'Email Address', 'User Name'])
        writer.writerows(students)

    # Writing lecturer data to CSV
    with open('lecturers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Lecturer ID', 'Lecturer Name', 'Email Address', 'User Name', 'Department'])
        writer.writerows(lecturers)

    # Writing grades data to CSV
    with open('grades.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student ID', 'Course Code', 'Grade'])
        writer.writerows(grades_flat)
        
    # Writing course data to CSV
    with open('courses.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Course Code', 'Course Name', 'Department', 'Start Date', 'End Date'])
        writer.writerows(courses)
        
    # Writing schedule data to CSV    
    with open('lecturer_schedules.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Lecturer ID', 'Course Code', 'Department'])
        writer.writerows(lecturer_schedules)

    print("Data generated and written to CSV files: students.csv, lecturers.csv, grades.csv, courses.csv and lecturer_schedules.csv")

except Exception as e:
    print(f"An error occurred: {e}")
