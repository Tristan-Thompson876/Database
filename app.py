from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'TrissSQL9845',
    'host': '127.0.0.1',
    'database': 'School_System'
}

def ServerConnection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

@app.route('/Register', methods=['PUT'])
def Register_User():
    try:
        connection = ServerConnection()
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(UserID) FROM Account")
        max_id = cursor.fetchone()[0]
        new_id = max_id + 1 if max_id else 1

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
def User_Login():
    try:
        uname = request.args.get('uname')
        upass = request.args.get('password')

        connection = ServerConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Account WHERE Username=%s AND Password=%s", (uname, upass))

        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return make_response({"message": "Login successful", "user": user}, 200)
        else:
            return make_response({"error": "Invalid credentials"}, 401)
    except Exception as e:
        return make_response({'error': f'An error has occurred: {str(e)}'}, 400)

@app.route('/add_Course', methods=['POST'])
def create_Course():
    try:
        connection = ServerConnection()
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

@app.route('/find_Course/<cName>', methods=['GET'])
def get_Course(cName):
    try:
        connection = ServerConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT CourseCode, CourseName, StartDate, EndDate FROM Course WHERE CourseName=%s", (cName,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if row:
            CourseCode, CourseName, StartDate, EndDate = row
            course = {"CourseCode": CourseCode, "CourseName": CourseName, "StartDate": StartDate, "EndDate": EndDate}
            return make_response(course, 200)
        else:
            return make_response({'error': 'Course not found'}, 404)
    except Exception as e:
        return make_response({'error': f'An error has occurred: {str(e)}'}, 500)

@app.route('/register_course', methods=['POST'])
def register_course():
    data = request.json
    student_id = data.get('student_id')
    course_code = data.get('course_code')

    if not is_valid_registration(student_id, course_code):
        return jsonify({'message': 'Invalid registration data'}), 400

    try:
        connection = ServerConnection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO StudentCourses (StudentID, CourseCode) VALUES (%s, %s)", (student_id, course_code))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Registration successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Error registering for course', 'error': str(e)}), 500

def is_valid_registration(student_id, course_code):
    connection = ServerConnection()
    cursor = None
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Student WHERE StudentID = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            return False

        cursor.execute("SELECT * FROM Course WHERE CourseC = %s", (course_code,))
        course = cursor.fetchone()
        if not course:
            return False

        cursor.execute("SELECT * FROM LecturerAssignments WHERE CourseC = %s", (course_code,))
        lecturer_assignment = cursor.fetchone()
        if not lecturer_assignment:
            return False

        return True
    except Exception as e:
        print("Error checking registration validity:", e)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route('/course-members/<course_code>', methods=['GET'])
def get_CourseMembers(course_code):
    try:
        connection = ServerConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Student WHERE StudentID IN (SELECT StudentID FROM Enroll WHERE CourseC=%s)", (course_code,))
        students = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(students), 200
    except mysql.connector.Error as err:
        return jsonify({'error': f"An error has occurred: {err}"}), 500

@app.route('/calendar-events', methods=['GET'])
def get_CalendarEvents():
    try:
        connection = ServerConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Calendar")
        rows = cursor.fetchall()
        events = []
        for row in rows:
            EventID, CourseID, Title, SDate, EDate = row
            event = {'EventID': EventID, 'CourseID': CourseID, 'Title': Title, 'SDate': SDate, 'EDate': EDate}
            events.append(event)
        cursor.close()
        connection.close()
        return jsonify(events), 200
    except Exception as e:
        return make_response({'error': f'An error has occurred: {str(e)}'}, 500)

@app.route('/create_calendar-events', methods=['POST'])
def create_CalendarEvents():
    try:
        connection = ServerConnection()
        cursor = connection.cursor()

        content = request.json
        CourseID = content.get('CourseID')
        Title = content.get('Title')
        SDate = content.get('SDate')
        EDate = content.get('EDate')

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
    connection = ServerConnection()
    if connection is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    try:
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
        connection.close()

@app.route('/enroll', methods=['POST'])
def enroll_student():
    try:
        data = request.json
        student_id = data.get('student_id')
        course_code = data.get('course_code')

        connection = ServerConnection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Enroll (StudentID, CourseC) VALUES (%s, %s)", (student_id, course_code))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Student enrolled successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error enrolling student', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=4000)
