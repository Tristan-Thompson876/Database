import csv
import random
from faker import Faker
from faker.providers import BaseProvider


# For generating student information

class StudentProvider(BaseProvider):
    
    def studentalia(self):
        gender = self.random_element(["F", "M"])
        first_name = self.generator.first_name_male() if gender == "M" else self.generator.first_name_female()
        last_name = self.generator.last_name()
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (first_name, last_name, email_address, user_name)
        
fake = Faker()
fake.add_provider(StudentProvider)

student = [fake.studentalia() for per in range(10)]

print(student) # generated list of student particulars


# For generating lecturer information

class LecturerProvider(BaseProvider):
    
    def lectureralia(self):
        gender = self.random_element(["F", "M"])
        title = self.generator.prefix_male() if gender == "M" else self.generator.prefix_female()
        first_name = self.generator.first_name_male() if gender == "M" else self.generator.first_name_female()
        last_name = self.generator.last_name()
        email_address = f"{first_name.lower()}.{last_name.lower()}@{'user.myschooly.com'}"
        user_name = f"{first_name}_{last_name}"
        
        return (title, first_name, last_name, email_address, user_name)
        
fake = Faker()
fake.add_provider(LecturerProvider)

lecturer = [fake.lectureralia() for per in range(55)]

print(lecturer) # generated list of lecturer particulars

# For generating courses and course codes

Courses = ['MATH', 'SOCI', 'LING', 'BIO', 'CHEM', 'PHYS', 'MEDI', 'PSYCH', 'ECON', 'ACCT', 'POLI']
CourseN = ['Mathematics', 'Sociology', 'Linguistics', 'Biology', 'Chemistry', 'Physics', 'Medicine', 'Psychology', 'Economics', 'Accounting', 'Political Science']

ccdict = {course_name: [course + str(random.randint(1000, 6501)) for _ in range(20)] for course, course_name in zip(Courses, CourseN)}
print(ccdict) # dictionary generating 200 courses with 10 different areas of study: 20 courses each from lvl 1 to lvl 6

# Iterate over the student list and assign random courses ######## CONTINUE TO EDIT CODE FROM THIS LINE DOWN!!!!!
for s in student:
    random_course_keys = random.choices(Courses, k=random.randint(4, min(6, len(Courses))))
    random_courses = [random.choice(ccdict[key]) for key in random_course_keys]
    s.extend(random_courses)

# Print the modified student list
print(student)

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

print("Data generated and written to CSV files: students.csv and lecturers.csv")

####### TAKE NOTE: Code is still incomplete, but if currently ran, it would generate student and lecturer data and write them to two seperate csv files ######
