from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash
from models import db
from models.user import User, Student, Admin, Course, Enrollment
# from flask_migrate import Migrate


app = Flask(__name__, static_folder='static')
app.secret_key = "test 2342345"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:test12345@localhost/school"
db.init_app(app)
# migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # db.drop_all()
    db.create_all()
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       user = User.query.filter_by(username=username).first()
       if user and user.check_password(password):
           session['user_id'] = user.id
           session['role'] = user.role
           return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'student_dashboard'))
       flash("Invalid Username or Password")
       
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email= request.form['email']
        username = request.form['username']
        password = request.form['password']
        role=request.form['role']

        is_user = User.query.filter_by(username=username).first()
        if is_user:
            flash("Username already exists. Please login.")
            return render_template('signup.html')
        
        user = User(name=name, email=email, username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        new_admin = Admin(name=name, user_id=user.id)
        db.session.add(new_admin)
        
        db.session.commit()
        flash("Account created successfully, Please login.")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# @app.route('/admin', methods=['GET', 'POST'])
# def admin_dashboard():
#     if 'user_id' in session and session['role'] == 'admin':
#         if request.method == 'POST':
#             name = request.form['name']
#             student_id = request.form['student_id']
#             courses = request.form['courses']
#             username = request.form['username']
#             password = request.form['password']

#             user = User(name=name, email=f"{username}@gmail.com", username=username, role='student')
#             user.set_password(password)
#             db.session.add(user)
#             db.session.commit()

#             new_student = Student(name=name, student_id=student_id, courses=courses, user_id=user.id, created_by = session['user_id'])
#             db.session.add(new_student)
#             db.session.commit()
#             flash("Student added successfully")
#         students = Student.query.all()
#         admin = Admin.query.filter_by(user_id=session['user_id']).first()
#         return render_template('admin.html', students=students, admin=admin)
#     return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    print(request.form)
    if 'user_id' in session and session['role'] == 'admin':
        if request.method == 'POST':
            if 'student_form' == request.form.get('form_name'):
                # Handle student creation
                name = request.form['name']
                student_id = request.form['student_id']
                courses = request.form['courses']
                username = request.form['username']
                password = request.form['password']

                user = User(name=name, email=f"{username}@gmail.com", username=username, role='student')
                user.set_password(password)
                db.session.add(user)
                db.session.commit()

                new_student = Student(name=name, student_id=student_id, courses=courses, user_id=user.id, created_by=session['user_id'])
                db.session.add(new_student)
                db.session.commit()
                flash("Student added successfully")
            elif 'course_form' == request.form.get('form_name'):
                # Handle course creation
                title = request.form['title']
                description = request.form['description']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                course = Course(title=title, description=description, start_date=start_date, end_date=end_date)
                db.session.add(course)
                db.session.commit()
                flash("Course created successfully")
        
        students = Student.query.all()
        courses = Course.query.all()
        admin = Admin.query.filter_by(user_id=session['user_id']).first()
        return render_template('admin.html', students=students, courses=courses, admin=admin)
    return redirect(url_for('login'))


@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_student(id):
    if 'user_id' in session and session['role'] == 'admin':
        student = Student.query.get(id)
        if student:
            user = User.query.get(student.user_id)
            if user:
                db.session.delete(student)
                db.session.delete(user)
                db.session.commit()
                flash("Student deleted successfully")
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user_id' in session and session['role'] == 'admin':
        student = Student.query.get(id)
        if request.method == 'POST':
            student.name = request.form['name']
            student.student_id = request.form['student_id']
            student.courses = request.form['courses']
            db.session.commit()
            flash("Student details updated successfully")
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_edit.html', student=student)
    return redirect(url_for('login'))

@app.route('/student')
def student_dashboard():
    if 'user_id' in session and session['role'] == 'student':
        student = Student.query.filter_by(user_id=session['user_id']).first()
        courses = Course.query.all()
        return render_template('student.html', student=student, courses=courses)
    return redirect(url_for('login'))

@app.route('/enroll/<int:course_id>', methods=['GET', 'POST'])
def enroll(course_id):
    if 'user_id' in session and session['role'] == 'student':
        user_id = session['user_id']
        student = Student.query.filter_by(user_id=user_id).first()
        enrollment = Enrollment(student_id=student.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash("Enrolled successfully")
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

@app.route('/courses')
def course_list():
    courses = Course.query.all()
    return render_template('course_list.html', courses=courses)

@app.route('/courses/new', methods=['GET', 'POST'])
def new_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        course = Course(title=title, description=description, start_date=start_date, end_date=end_date)
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully')
        return redirect(url_for('course_list'))
    return render_template('new_course.html')

@app.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        course.title = request.form['title']
        course.description = request.form['description']
        course.start_date = request.form['start_date']
        course.end_date = request.form['end_date']
        db.session.commit()
        flash('Course updated successfully')
        return redirect(url_for('course_list'))
    return render_template('edit_course.html', course=course)

@app.route('/course/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully')
    return redirect(url_for('course_list'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)