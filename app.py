from flask import Flask, request, make_response
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'TrissSQL9845',
    'host': '127.0.0.1',
    'database': 'your_database'
}

def ServerConnection(user = '', password = '', host = '', database = ''):
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection



@app.route('/Register', methods=['PUT'])
def Register_User(uname, upass):
    try:
        connection = ServerConnection(db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(UserID) FROM Account")
        max_id = cursor.fetchone()[0]
        new_id = max_id + 1

        content = request.json
        username = content.get('Username')
        password = content.get('Password')

        cursor.execute("INSERT INTO Account (UserID, Username, Password) VALUES (%s, %s, %s)", (new_id, username, password))
        connection.commit()
        cursor.close()

        return make_response({"success": "User registered successfully", "UserID": new_id}, 202)
    except mysql.connector.Error as err:
        return make_response({'error': f"An error occurred: {err}"}, 400)
    finally:
        if connection is not None:
            connection.close() 

@app.route('/Userlogin', methods=['GET'])
def User_Login(uname, upass):
    try:
        connection = ServerConnection(db_config)

        cursor = connection.cursor()
        cursor.excecute(f"SELECT * FROM Account WHERE Username={uname} AND password={upass}")
        #make_response
        cursor.close
    except:
        return make_response({'error': 'An error has occured'}, 400)

@app.route('/add_Course', methods=['POST'])
def create_Course():
    try:
        connection = ServerConnection(db_config)
        cursor = connection.cursor()

        content = request.json
        CourseC = content.get('CourseC')
        CourseName = content.get('CourseName')
        StartDt = content.get('StartDt')
        EndDt = content.get('EndDt')

        cursor.execute("INSERT INTO Course (CourseC, CourseName, StartDt, EndDt) VALUES (%s, %s, %s, %s)", (CourseC, CourseName, StartDt, EndDt))
        connection.commit()
        cursor.close()

        return make_response({"success": "Course added successfully"}, 200)
    except mysql.connector.Error as err:
        return make_response({'error': f"An error occurred: {err}"}, 400)
    finally:
        if connection is not None:
            connection.close()

@app.route('/find_Course', methods=['GET'])
def get_Course(cName):
    try:
        connection = ServerConnection(db_config)

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM Course WHERE courseName={cName}")
        row = cursor.fetchone()
        course = {}
        if row is not None:
            CourseC, CourseName, StartDt, EndDt = row
            course["Coursec"] = CourseC
            course["CourseName"] = CourseName
            course["StartDt"] = StartDt
            course["EndDt"] = EndDt
            cursor.close()
            return make_response(course, 200)
        else:
            return make_response({'error': "Anerror has occured"}, 400)

    except:
        return make_response({'error': 'An error has occured'}, 400)

@app.route()
def Course_Register():
    connection = ServerConnection(db_config)
    return

@app.route()
def get_CourseMembers():
    try:
        connection = ServerConnection(db_config)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Student WHERE STudentID IN (SELECT StudentID FROM Assignments WHERE CourseC=%s)", (CourseC))
        students = cursor.fethchall()
        cursor.close()
        return jsonify(students), 200
    except:
        return jsonify({'error': f"An error has occurred: {err}"}), 500

    finally:
        if connection is not None:
            connection.close()

@app.route()
def get_CalendarEvents():
    try:
        connection = ServerConnection(db_config)
        
        cursor = connection.cursor()
        cursor.excecute(f"SELECT * FROM Calendar")
        row = cursor.fetchone
        events = {}
        if row is not None:
            EventID, CourseID, Title, SDate, EDate = row
            events['EventID'] = EventID
            events['CourseID'] = CourseID
            events['Title'] = Title
            events['SDate'] = SDate
            events['EDate'] = EDate
            cursor.close()
            return make_response(events, 200)
        else:
            return make_response({'error': 'Student not found'}, 400)
    except:
        return make_response({'error': 'An error has occured'}, 400)

@app.route()
def create_CalendarEvents(CourseID, Title, SDate, EDate):
    try:
        connection = ServerConnection(db_config)
        cursor = connection.cursor()

        #content = request.jsonCourseID = content.get('CourseID')Title = content.get('Title')SDate = content.get('SDate')EDate = content.get('EDate')
        cursor.execute("INSERT INTO Calendar (CourseID, Title, SDate, EDate) VALUES (%s, %s, %s, %s)", (CourseID, Title, SDate, EDate))
        connection.commit()
        cursor.close()

        return make_response({"success": "Calendar event created successfully"}, 200)
    except mysql.connector.Error as err:
        return make_response({'error': f"An error occurred: {err}"}, 400)
    finally:
        if connection is not None:
            connection.close()

@app.route('/manage_forums', methods=['GET', 'POST'])
def manage_Forums():
    connection = ServerConnection(db_config)
    if connection is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    if request.method == 'GET':
        course_code = request.args.get('course_code')
        if not course_code:
            return jsonify({"message": "Course code is required for retrieving forums"}), 400
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM DiscussionForum WHERE CourseC = %s"
            cursor.execute(query, (course_code,))
            forums = cursor.fetchall()
            cursor.close()
            return jsonify({"forums": forums}), 200
        except Error as e:
            return jsonify({"message": f"Failed to retrieve forums: {e}"}), 500

    elif request.method == 'POST':
        data = request.get_json()
        course_code = data.get('course_code')
        forum_name = data.get('forum_name')
        if not course_code or not forum_name:
            return jsonify({"message": "Course code and forum name are required for creating a forum"}), 400
        try:
            cursor = connection.cursor()
            query = "INSERT INTO DiscussionForum (CourseC, Name) VALUES (%s, %s)"
            cursor.execute(query, (course_code, forum_name))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Forum created successfully"}), 201
        except Error as e:
            return jsonify({"message": f"Failed to create forum: {e}"}), 500
        finally:
            if connection.is_connected():
                connection.close()


@app.route()
def manage_DiscussionThread():
    connection = ServerConnection(db_config)
    if connection is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    if request.method == 'GET':
        forum_id = request.args.get('forum_id')
        if not forum_id:
            return jsonify({"message": "Forum ID is required for retrieving discussion threads"}), 400
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM DiscussionThread WHERE DiscussionForumID = %s"
            cursor.execute(query, (forum_id,))
            threads = cursor.fetchall()
            cursor.close()
            return jsonify({"discussion_threads": threads}), 200
        except Error as e:
            return jsonify({"message": f"Failed to retrieve discussion threads: {e}"}), 500

    
    elif request.method == 'POST':
        data = request.get_json()
        forum_id = data.get('forum_id')
        student_id = data.get('student_id')
        title = data.get('title')
        content = data.get('content')
        if not forum_id or not student_id or not title or not content:
            return jsonify({"message": "Forum ID, student ID, title, and content are required for adding a thread"}), 400
        try:
            cursor = connection.cursor()
            query = "INSERT INTO DiscussionThread (DiscussionForumID, StudentID, Title, Content) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (forum_id, student_id, title, content))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Discussion thread added successfully"}), 201
        except Error as e:
            return jsonify({"message": f"Failed to add discussion thread: {e}"}), 500

    
    elif request.method == 'PUT':
        data = request.get_json()
        thread_id = data.get('thread_id')
        student_id = data.get('student_id')
        reply_content = data.get('reply_content')
        if not thread_id or not student_id or not reply_content:
            return jsonify({"message": "Thread ID, student ID, and reply content are required for adding a reply"}), 400
        try:
            cursor = connection.cursor()
            query = "INSERT INTO DiscussionReply (DiscussionThreadID, StudentID, Content) VALUES (%s, %s, %s)"
            cursor.execute(query, (thread_id, student_id, reply_content))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Reply added successfully"}), 201
        except Error as e:
            return jsonify({"message": f"Failed to add reply: {e}"}), 500
        finally:
            if connection.is_connected():
                connection.close()

@app.route('/manage_course_content', methods=['POST', 'GET'])
def manage_CourseContent(CourseC):
    connection = ServerConnection(db_config)
    if connection is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    if request.method == 'POST':
        data = request.get_json()
        course_code = data.get('course_code')
        section = data.get('section')
        content_type = data.get('content_type')
        content = data.get('content')
        if not course_code or not section or not content_type or not content:
            return jsonify({"message": "Course code, section, content type, and content are required for adding course content"}), 400
        try:
            cursor = connection.cursor()
            query = "INSERT INTO CourseContent (CourseC, Section, ContentType, Content) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (course_code, section, content_type, content))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Course content added successfully"}), 201
        except Error as e:
            return jsonify({"message": f"Failed to add course content: {e}"}), 500

    elif request.method == 'GET':
        course_code = request.args.get('course_code')
        if not course_code:
            return jsonify({"message": "Course code is required for retrieving course content"}), 400
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM CourseContent WHERE CourseC = %s"
            cursor.execute(query, (course_code,))
            course_content = cursor.fetchall()
            cursor.close()
            return jsonify({"course_content": course_content}), 200
        except Error as e:
            return jsonify({"message": f"Failed to retrieve course content: {e}"}), 500
        finally:
            if connection.is_connected():
                connection.close()

@app.route()
def manage_Assignments():
    connection = ServerConnection(db_config)
    if connection is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    if request.method == 'POST':
        data = request.get_json()
        course_code = data.get('course_code')
        title = data.get('title')
        description = data.get('description')
        submission = data.get('submission')
        due_date = data.get('due_date')
        if not course_code or not title or not description or not submission or not due_date:
            return jsonify({"message": "Course code, title, description, submission, and due date are required for submitting assignment"}), 400
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Assignments (CourseC, Title, Description, Submission, DueDate) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (course_code, title, description, submission, due_date))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Assignment submitted successfully"}), 201
        except Error as e:
            return jsonify({"message": f"Failed to submit assignment: {e}"}), 500

    
    elif request.method == 'PUT':
        data = request.get_json()
        assignment_id = data.get('assignment_id')
        student_id = data.get('student_id')
        grade = data.get('grade')
        if not assignment_id or not student_id or not grade:
            return jsonify({"message": "Assignment ID, student ID, and grade are required for submitting grade"}), 400
        try:
            cursor = connection.cursor()
            query = "UPDATE Assignments SET Grade = %s WHERE AssignmentID = %s AND StudentID = %s"
            cursor.execute(query, (grade, assignment_id, student_id))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Grade submitted successfully"}), 200
        except Error as e:
            return jsonify({"message": f"Failed to submit grade: {e}"}), 500
        finally:
            if connection.is_connected():
                connection.close()

@app.route()
def make_Reports():
    connection = ServerConnection(db_config)
    if connection is None:
        return jsonify({"message": "Failed to connect to the database"}), 500
    
    create_views(connection)
    
    return jsonify({"message": "Reports generated successfully"}), 200


def create_views(connection):
    try:
        cursor = connection.cursor()
        # All courses that have 50 or more students
        cursor.execute("""
            CREATE VIEW CoursesWith50OrMoreStudents AS
            SELECT CourseC, COUNT(*) AS StudentCount
            FROM Enroll
            GROUP BY CourseC
            HAVING COUNT(*) >= 50
        """)
        
        # All students that do 5 or more courses
        cursor.execute("""
            CREATE VIEW StudentsWith5OrMoreCourses AS
            SELECT StudentID, COUNT(*) AS CourseCount
            FROM Enroll
            GROUP BY StudentID
            HAVING COUNT(*) >= 5
        """)
        
        # All lecturers that teach 3 or more courses
        cursor.execute("""
            CREATE VIEW LecturersWith3OrMoreCourses AS
            SELECT LecturerID, COUNT(*) AS CourseCount
            FROM Course
            GROUP BY LecturerID
            HAVING COUNT(*) >= 3
        """)
        
        # The 10 most enrolled courses
        cursor.execute("""
            CREATE VIEW Top10EnrolledCourses AS
            SELECT CourseC, COUNT(*) AS EnrollmentCount
            FROM Enroll
            GROUP BY CourseC
            ORDER BY EnrollmentCount DESC
            LIMIT 10
        """)
        
        # The top 10 students with the highest overall averages
        cursor.execute("""
            CREATE VIEW Top10StudentsHighestOverallAvg AS
            SELECT StudentID, AVG(Grade) AS OverallAvg
            FROM Grades
            GROUP BY StudentID
            ORDER BY OverallAvg DESC
            LIMIT 10
        """)
        
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating views: {e}")
if __name__ == '__main__':
    app.run(debug = True,port=3000)
