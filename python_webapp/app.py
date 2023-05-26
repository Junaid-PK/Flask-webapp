# 3 types of accounts :

# 1, Admin Type :
# 2, Professor Type 
# 3, Student Type 

# Whenever opening the link this should start up first.
# Sign in & option to Sign up. ( Make sure that that each type of account has a different introduction page when signing in)
# After the user logs in or signs up.

# Student :
# Courses and modules :

# 1, Blackboard -> ( Access to this link instantly -> https://blackboard.buid.ac.ae/)
# 2, Class timetable ( shows the student to have a calender of this semesters timetable)
# 3, Add/drop courses (Ability to Add/drop courses, make it simplified and make the user confirm it before adding/dropping, maximum of 4 modules that can be taken per semester)  MAKE SURE OF THIS -> (Make sure that the student doesn't have permission to take a class that he does not have the prerequisite for.)
# 4, Module Feedback ( Opens a sheet form that prompts you to give feedback regarding the modules you are taking, drop down menu to show the student his current timetable)
# 5, Online enrolment ( A simple page that tells the user the next semesters modules, and if he'd like to enroll in them, also prompt him to enroll)



# Exams, Assesment and Appeals :

# 1, Your Progress (Shows how many credits left for the student to graduate, and how many credits he has currently, approx how many months/years
# until he graduates from unviersity) 
# 2, Exams Timetable ( Shows timetables for final exams with their dates and the time they start and finish, Each final exam should be 2 hours 45 minutes) 
# 3, Results ( Shows results of past & current courses, following a picture that i will send you)
# 4, File an appeal. ( Opens up a page that asks what type of appeal you're looking for, will send you a screenshot regarding everything here.)



# Student Services :

# It Services ( Opens up your email and inputs the email "itservices@buid.ac.ae" as the receiver, and then the user can put their issue into the email.)
# Library Services (Opens up your email and inputs the email "library@buid.ac.ae" as the receiver, and then the user can put their prompt into the email.)
# Printing Services ( opens up this link "https://print.buid.ac.ae/")
# Blackboard Support ( Opens up your email and inputs the email "itservices@buid.ac.ae" as the receiver, and then the user can put their issue into the email.)


# Professor :

# Add/Drop courses to students by student ID (When student registers they have a specific ID, then the professor can add/remove the student by their ID if needed)
# Manage course timings  (Let professor be able to change course timings of the classes he teaches)
# Additional Classes (Let professor be able to add additional classes for students who are not doing well in university)




# Admin : Has access to everything, and can add/remove students from the database and can also add/remove professors from the database


from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'




# Configure the MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uni_db'

# Create a MySQL connection
mysql_conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# Create a cursor object
cursor = mysql_conn.cursor(buffered=True)

# Create a route for the home page
@app.route('/')
def home():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('student.html')

# Create a route for the signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Route for signup form submission
@app.route('/signup', methods=['POST'])
def signup_post():
    # get the data from the form
    print(request.form)
    name = request.form['name']
    username = request.form['Username']
    password = request.form['password']
    cpassword = request.form['cpassword']
    type = "Student"

    # Check if the passwords match
    if password != cpassword:
        return redirect(url_for('signup'))
    
    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    if user:
        return redirect(url_for('signup'))
    
    # Insert the user into the database
    cursor.execute('INSERT INTO users (name, username, password, role) VALUES (%s, %s, %s, %s)', (name, username, password, type))
    mysql_conn.commit()

    return redirect(url_for('login'))

# Create a route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for login form submission
@app.route('/login', methods=['POST'])
def login_post():
    # get the data from the form
    username = request.form['Username']
    password = request.form['password']

    # Check if the username exists
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    if not user:
        return redirect(url_for('login'))
    
    # Check if the password is correct
    if password != user[3]:
        return redirect(url_for('login'))
    
    # save the user in the session
    session['user'] = user
    
    # Redirect to the correct page based on the role
    if user[4] == 'Student':
        return redirect(url_for('student'))
    elif user[4] == 'Professor':
        return redirect(url_for('professor'))
    elif user[4] == 'Admin':
        return redirect(url_for('admin'))
    
    return redirect(url_for('login'))

# Create a route for the student page
@app.route('/student')
def student():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']
    
    # Check if the user is a student
    if user[4] == 'Student':
        return redirect(url_for('student'))
    elif user[4] == 'Professor':
        return redirect(url_for('professor'))
    elif user[4] == 'Admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))
    
    return render_template('student.html', user=user)

# Create a route for the professor page
@app.route('/professor')
def professor():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']
    
    # Check if the user is a professor
    if user[4] != 'Professor':
        return redirect(url_for('login'))
    
    return render_template('professor.html', user=user)

# Create a route for the admin page
@app.route('/admin')
def admin():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']
    
    # Check if the user is an admin
    if user[4] != 'Admin':
        return redirect(url_for('login'))
    
    return render_template('admin.html', user=user)

# Create a route for the logout page
@app.route('/logout')
def logout():
    # Remove the user from the session
    session.pop('user', None)
    return redirect(url_for('login'))

# Create a route for the timetable page
@app.route('/timetable')
def timetable():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']
    
    # Check if the user is a student
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Get the timetable from the database
    cursor.execute('SELECT * FROM class_timetable')
    timetable = cursor.fetchall()
    print(timetable)
    
    return render_template('timetable.html', user=user, timetable=timetable)

# Create a route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']
    
    # Check if the user is a student
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    return render_template('student.html', user=user)

# Create a route for the add/drop page
@app.route('/modify-courses')
def add_drop():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']

    # Check if the user is a student
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Get the courses from the database
    cursor.execute('SELECT course_id,course_code, name FROM course_enrollment JOIN courses ON course_enrollment.course_id = courses.id WHERE student_id = %s', (user[0],))
    courses = cursor.fetchall()
    
    
    return render_template('add_drop.html', user=user, courses=courses)

# Create a route for the add/drop form submission
@app.route('/modify_course/<int:course_id>')
def add_drop_post(course_id):
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']

    # Check if the user is a student
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Check if the course exists
    cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
    course = cursor.fetchone()
    if not course:
        return redirect(url_for('add_drop'))
    
    # Check if the user is already enrolled in the course
    cursor.execute('SELECT * FROM course_enrollment WHERE student_id = %s AND course_id = %s', (user[0], course_id,))
    enrollment = cursor.fetchone()
    if enrollment:
        # Drop the course
        cursor.execute('DELETE FROM course_enrollment WHERE student_id = %s AND course_id = %s', (user[0], course_id,))
        mysql_conn.commit()
    return redirect(url_for('add_drop'))

# Create a route for the module feedback page
@app.route('/module-feedback')
def module_feedback():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']

    # Check if the user is a student
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Get the courses from the database
    cursor.execute('SELECT course_id,course_code, name FROM course_enrollment JOIN courses ON course_enrollment.course_id = courses.id WHERE student_id = %s', (user[0],))
    courses = cursor.fetchall()

    # Check if the user has already given feedback for the course
    cursor.execute('SELECT * FROM feedback WHERE student_id = %s', (user[0],))
    feedback = cursor.fetchone()
    feedback_given = False
    if feedback:
        feedback_given = True

    
    
    return render_template('module_feedback.html', user=user, courses=courses, feedback_given=feedback_given)

# Create a route for the module feedback form submission
@app.route('/feedback/<int:course_id>')
def module_feedback_post(course_id):
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']

    # Check if the user is a student
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Check if the course exists
    cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
    course = cursor.fetchone()
    if not course:
        return redirect(url_for('module_feedback'))
    
    # Check if the user is already enrolled in the course
    cursor.execute('SELECT * FROM course_enrollment WHERE student_id = %s AND course_id = %s', (user[0], course_id,))
    enrollment = cursor.fetchone()
    if not enrollment:
        return redirect(url_for('module_feedback'))
    
    return render_template('feedback.html', user=user, course=course)

# Create a route for the module feedback form submission
@app.route('/feedback/<int:course_id>', methods=['POST'])
def module_feedback_post_submit(course_id):
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the user from the session
    user = session['user']

    # Check if the user is a student
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Check if the course exists
    cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
    course = cursor.fetchone()
    if not course:
        return redirect(url_for('module_feedback'))
    
    # Check if the user is already enrolled in the course
    cursor.execute('SELECT * FROM course_enrollment WHERE student_id = %s AND course_id = %s', (user[0], course_id,))
    enrollment = cursor.fetchone()
    if not enrollment:
        return redirect(url_for('module_feedback'))
    
    # Get the data from the form
    feedback = request.form['feedback']

    # Insert the feedback into the database
    cursor.execute('INSERT INTO feedback (student_id, course_id, feedback) VALUES (%s, %s, %s)', (user[0], course_id, feedback))
    mysql_conn.commit()

    return redirect(url_for('module_feedback'))

# Create a route for the online enrollment page
@app.route('/online-enrollment')
def online_enrollment():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is a student
    user = session['user']
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Get the courses from the database and set buffered to true
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()


    
    # Get the courses the user is enrolled in
    cursor.execute('SELECT course_id FROM course_enrollment WHERE student_id = %s', (user[0],))
    enrollments = cursor.fetchall()
    enrollments = [enrollment[0] for enrollment in enrollments]

    # remove the courses the user is already enrolled in
    courses = [course for course in courses if course[0] not in enrollments]

    # remove the courses that are not available for the student's major
    cursor.execute('SELECT student_id,program_id FROM student_programs WHERE student_id = %s', (user[0],))
    student = cursor.fetchone()
    cursor.execute('SELECT id FROM courses WHERE program_id = %s', (student[1],))
    program_courses = cursor.fetchall()

    program_courses = [course[0] for course in program_courses]
    courses = [course for course in courses if course[0] in program_courses]



    return render_template('enrollment.html', user=user, courses=courses)

# Create a route for the online enrollment form submission
@app.route('/enrollment/<int:course_id>', methods=['POST'])
def online_enrollment_post(course_id):
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is a student
    user = session['user']
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Check if the course exists
    cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
    course = cursor.fetchone()
    if not course:
        return redirect(url_for('online_enrollment'))
    
    # Check if the user is already enrolled in the course
    cursor.execute('SELECT * FROM course_enrollment WHERE student_id = %s AND course_id = %s', (user[0], course_id,))
    enrollment = cursor.fetchone()
    if enrollment:
        return redirect(url_for('online_enrollment'))
    
    # Insert the enrollment into the database
    cursor.execute('INSERT INTO course_enrollment (student_id, course_id) VALUES (%s, %s)', (user[0], course_id))
    mysql_conn.commit()
    return redirect(url_for('online_enrollment'))

# Create a route for the Progress page
@app.route('/progress')
def progress():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is a student
    user = session['user']
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Get the courses from the database
    cursor.execute('SELECT course_id FROM course_enrollment WHERE student_id = %s', (user[0],))
    courses = cursor.fetchall()
    courses = [course[0] for course in courses]

    # Get the credits of the courses
    # covert the list of courses using join
    cursor.execute('SELECT credits FROM courses WHERE id IN (%s)' % ','.join(map(str, courses)))
    credits = cursor.fetchall()
    credits = [credit[0] for credit in credits]


    # Get the total credits
    total_credits = sum(credits)

    # Get the total credits required
    cursor.execute('SELECT credits_required FROM student_programs WHERE student_id = %s', (user[0],))
    credits_required = cursor.fetchone()[0]
    

    # Get the total credits remaining
    credits_remaining = credits_required - total_credits
    print(user)
    # Get the total semesters remaining
    cursor.execute('SELECT semesters_required FROM student_programs WHERE student_id = %s', (user[0],))
    semesters_required = cursor.fetchone()[0]
    print("semesters required", semesters_required)

    # Get the total semesters remaining
    cursor.execute('SELECT semesters_completed FROM student_programs WHERE student_id = %s', (user[0],))
    semesters_completed = cursor.fetchone()[0]
    print("semesters completed", semesters_completed)

    # Get the total semesters remaining
    semesters_remaining = semesters_required - semesters_completed

    # Get the total years remaining
    years_remaining = semesters_remaining / 2

    return render_template('progress.html', user=user, total_credits=total_credits, credits_required=credits_required, credits_remaining=credits_remaining, semesters_required=semesters_required, semesters_completed=semesters_completed, semesters_remaining=semesters_remaining, years_remaining=years_remaining)

# Create a route for the exams page
@app.route('/exams')
def exams():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is a student
    user = session['user']
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Get the exams from the database
    cursor.execute('SELECT name, course_code, exam_date, start_time, end_time FROM examstimetable JOIN courses ON examstimetable.course_id = courses.id WHERE student_id = %s', (user[0],))
    exams = cursor.fetchall()
    return render_template('exams.html', user=user, exams=exams)

# Create a route for the results page
@app.route('/results')
def results():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is a student
    user = session['user']
    if user[4] != 'Student':
        return redirect(url_for('login'))
    
    # Get the results from the database
    cursor.execute('SELECT name, course_code, total_marks, marks_recieved,grade FROM results JOIN courses ON results.course_id = courses.id WHERE student_id = %s', (user[0],))
    results = cursor.fetchall()
    return render_template('results.html', user=user, results=results)

# Create a route for admin manage students
@app.route('/manageStudents')
def manageStudents():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is an admin
    user = session['user']
    if user[4] != 'Admin':
        return redirect(url_for('login'))
    
    # Get the students from the database
    cursor.execute('SELECT * FROM users WHERE role = "Student"')
    students = cursor.fetchall()
    return render_template('manageStudents.html', user=user, students=students)

# Create a route for admin manage professors
@app.route('/manageProfessors')
def manageProfessors():

    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is an admin
    user = session['user']
    if user[4] != 'Admin':
        return redirect(url_for('login'))
    
    # Get the professors from the database
    cursor.execute('SELECT * FROM users WHERE role = "Professor"')
    professors = cursor.fetchall()

    return render_template('manageProfessors.html', user=user, professors=professors)

# Create a route for remove student
@app.route('/removeStudent/<int:student_id>')
def removeStudent(student_id):
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the student exists
    cursor.execute('SELECT * FROM users WHERE id = %s', (student_id,))
    student = cursor.fetchone()
    if not student:
        return redirect(url_for('manageStudents'))
    
    # Check if the user is an admin
    user = session['user']
    if user[4] != 'Admin':
        return redirect(url_for('login'))
    
    # Delete the student from the database
    cursor.execute('DELETE FROM users WHERE id = %s', (student_id,))
    mysql_conn.commit()
    return redirect(url_for('manageStudents'))

# Create a route for remove professor
@app.route('/removeProfessor/<int:professor_id>')
def removeProfessor(professor_id):

    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the professor exists
    cursor.execute('SELECT * FROM users WHERE id = %s', (professor_id,))
    professor = cursor.fetchone()
    if not professor:
        return redirect(url_for('manageProfessors'))
    
    # Check if the user is an admin
    user = session['user']
    if user[4] != 'Admin':
        return redirect(url_for('login'))
    
    # Delete the professor from the database
    cursor.execute('DELETE FROM users WHERE id = %s', (professor_id,))
    mysql_conn.commit()
    return redirect(url_for('manageProfessors'))

# Create a route for add student
@app.route('/addStudents')
def addStudent():

    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is an admin
    user = session['user']
    if user[4] != 'Admin':
        return redirect(url_for('login'))
    
    return render_template('addStudent.html', user=user)

# Create a route for add student form submission
@app.route('/addStudent', methods=['POST'])
def addStudent_post():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the data from the form
    name = request.form['name']
    username = request.form['Username']
    password = request.form['password']
    cpassword = request.form['cpassword']
    type = "Student"

    # Check if the passwords match
    if password != cpassword:
        return redirect(url_for('addStudent'))
    
    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    if user:
        return redirect(url_for('addStudent'))
    
    # Insert the user into the database
    cursor.execute('INSERT INTO users (name, username, password, role) VALUES (%s, %s, %s, %s)', (name, username, password, type))
    mysql_conn.commit()

    return redirect(url_for('manageStudents'))

# Create a route for add professor
@app.route('/addProfessors')
def addProfessor():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is an admin
    user = session['user']
    if user[4] != 'Admin':
        return redirect(url_for('login'))
    
    return render_template('addProfessor.html', user=user)

# Create a route for add professor form submission
@app.route('/addProfessor', methods=['POST'])
def addProfessor_post():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the data from the form
    name = request.form['name']
    username = request.form['Username']
    password = request.form['password']
    cpassword = request.form['cpassword']
    type = "Professor"

    # Check if the passwords match
    if password != cpassword:
        return redirect(url_for('addProfessor'))
    
    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    if user:
        return redirect(url_for('addProfessor'))
    
    # Insert the user into the database
    cursor.execute('INSERT INTO users (name, username, password, role) VALUES (%s, %s, %s, %s)', (name, username, password, type))
    mysql_conn.commit()

    return redirect(url_for('manageProfessors'))

# Create a route for the Professor to manage courses
@app.route('/manageCourses')
def manageCourses():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if the user is a professor
    user = session['user']
    if user[4] != 'Professor':
        return redirect(url_for('login'))
    
    # Get the student's courses from the database
    cursor.execute('SELECT student_id FROM course_enrollment JOIN users ON course_enrollment.student_id = users.id WHERE role = "Student"')
    students = cursor.fetchall()
    students = [student[0] for student in students]

    # Get the courses from the database
    cursor.execute('SELECT * FROM course_enrollment JOIN courses ON course_enrollment.course_id = courses.id')
    courses = cursor.fetchall()
    return render_template('manageCourses.html', user=user, courses=courses)

# Create a route for the Professor to manage courses
@app.route('/manageCourses/<int:student_id>')
def manageCourses_student(student_id):
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Check if student exists
    cursor.execute('SELECT * FROM users WHERE id = %s', (student_id,))
    student = cursor.fetchone()
    if not student:
        return redirect(url_for('manageCourses'))
    
    # Check if the user is a professor
    user = session['user']
    if user[4] != 'Professor':
        return redirect(url_for('login'))
    
    # Get the student's courses from the database
    cursor.execute('SELECT * FROM course_enrollment JOIN courses ON course_enrollment.course_id = courses.id WHERE student_id = %s', (student_id,))
    courses = cursor.fetchall()
    return render_template('manageCourses_student.html', user=user, courses=courses, student=student)









if __name__ == '__main__':
    app.run(debug=True)