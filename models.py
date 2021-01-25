from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
#The class below is the one that allows for users to be remembered in session data
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    classes = db.relationship('Classroom', backref='teacher', lazy='dynamic')

    #What the fuck does this do?
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#This is the user loader function
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    #This line below is going to represent the authorship of a blog post. Check back on primary vs foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher_username = db.Column(db.String(64), index=True, unique=False)
    class_id = db.Column(db.String(64), index=True, unique=False)
    class_name = db.Column(db.String(64), index=True, unique=False)
    student_count = db.Column(db.Integer)
    class_code = db.Column(db.String(64), unique=False)

class Classes(db.Model):
    id = db.Column(db.String(64), primary_key=True, index=True, unique=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    class_code = db.Column(db.String(64), unique=False)


class Assignments(db.Model):
    #this is the unique assignment ID
    id = db.Column(db.String(64), primary_key=True)
    assignment_id = db.Column(db.String(64), index=True, unique=False)
    class_id = db.Column(db.String(64), index=True, unique=False)
    class_code = db.Column(db.String(64), unique=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.String(64), db.ForeignKey('LE_question_bank.question_id'), index=True, unique=False)
    content = db.Column(db.String(64), unique=False)
    exam = db.Column(db.String(64), unique=False)
    lab = db.Column(db.Integer, unique=False)
    standard = db.Column(db.Integer, unique=False)
    key_idea = db.Column(db.Integer, unique=False)
    question = db.Column(db.String(64), unique=False)
    question_description = db.Column(db.String(64), unique=False)
    question_link = db.Column(db.String(140), unique=False)
    correct_answer = db.Column(db.Integer, unique=False)
    short_answer = db.Column(db.String(64), unique=False)



class LE_question_bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(64), unique=True)
    content = db.Column(db.String(64), unique=False)
    exam = db.Column(db.String(64), unique=False)
    lab = db.Column(db.Integer, unique=False)
    standard = db.Column(db.Integer, unique=False)
    key_idea = db.Column(db.Integer, unique=False)
    question = db.Column(db.String(64), unique=False)
    question_desc = db.Column(db.String(64), unique=False)
    question_link = db.Column(db.String(140), unique=False)
    correct_answer = db.Column(db.Integer, unique=False)
    short_answer = db.Column(db.String(64), unique=False)



class StudentAssessmentResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), index=True, unique=False)
    assignment_id = db.Column(db.String(64), index=True, unique=False)
    question_id = db.Column(db.String(64), unique=False)
    correct_answer = db.Column(db.Integer, unique=False)
    student_answer = db.Column(db.Integer, unique=False)
    student_justification = db.Column(db.String(140), unique=False)
    assessment_score = db.Column(db.Integer, unique=False)
    standard = db.Column(db.Integer, unique=False)
    key_idea = db.Column(db.Integer, unique=False)
    question_desc = db.Column(db.String(64), unique=False)
    question_link = db.Column(db.String(140), unique=False)
    teacher_feedback = db.Column(db.String(280), unique=False)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), unique=True)

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), unique=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), unique=True)
