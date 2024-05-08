import mysql.connector

conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="OURVLE_db"
        )


# Query 1. Retrieve all the courses
def get_all_courses():
    cursor = conn.cursor()
    sql = "SELECT * FROM Course"
    cursor.execute(sql)
    all_courses = cursor.fetchall()
    cursor.close()
    return all_courses


# Query 2. Retrieve courses for a particular student
def get_student_courses( student_id):
    cursor = conn.cursor()
    sql = "SELECT Course.* FROM Course INNER JOIN StudentCourses ON Course.CourseC = StudentCourses.CourseC WHERE StudentCourses.StudentID = %s"
    cursor.execute(sql, (student_id,))
    student_courses = cursor.fetchall()
    cursor.close()
    return student_courses


# Query3. Retrieve courses taught by a particular lecturer
def get_lecturer_courses(lecturer_id):
    cursor = conn.cursor()
    sql = "SELECT * FROM Course WHERE LecturerID = %s"
    cursor.execute(sql, (lecturer_id,))
    lecturer_courses = cursor.fetchall()
    cursor.close()
    return lecturer_courses


# Query 4. Return members of a particular course
def get_course_members( course_code):
    cursor = conn.cursor()
    sql = "SELECT Student.* FROM Student INNER JOIN StudentCourses ON Student.StudentID = StudentCourses.StudentID WHERE StudentCourses.CourseC = %s"
    cursor.execute(sql, (course_code,))
    course_members = cursor.fetchall()
    cursor.close()
    return course_members


# Query 5. Retrieve all calendar events for a particular course.
def get_all_calendar_events_for_course(course_code):
    cursor = conn.cursor()
    sql = "SELECT * FROM Calendar WHERE CourseC = %s"
    cursor.execute(sql, (course_code,))
    all_events_for_course = cursor.fetchall()
    cursor.close()
    return all_events_for_course


# Query 6. Retrieve all calendar events for a particular date for a particular student.
def get_all_calender_events_for_student_on_date( student_id, date):
    cursor = conn.cursor()
    sql = "SELECT Calendar.* FROM Calendar INNER JOIN StudentCourses ON Calendar.CourseC = StudentCourses.CourseC WHERE StudentCourses.StudentID = %s AND StartDt = %s"
    cursor.execute(sql, (student_id, date))
    events_for_student_on_date = cursor.fetchall()
    cursor.close()
    return events_for_student_on_date


# Query 7. Retrieve all the forums for a particular course
def get_all_forums_for_course( course_code):
    cursor = conn.cursor()
    sql = "SELECT * FROM DiscussionForum WHERE CourseC = %s"
    cursor.execute(sql, (course_code,))
    discussion_forums = cursor.fetchall()
    cursor.close()
    return discussion_forums


# Query 8. Retrieve all the discussion threads for a particular forum
def get_all_discussion_threads_for_forum(forum_id):
    cursor = conn.cursor()
    sql = "SELECT * FROM DiscussionThread WHERE DiscussionForumID = %s"
    cursor.execute(sql, (forum_id,))
    discussion_threads = cursor.fetchall()
    cursor.close()
    return discussion_threads


