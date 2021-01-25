#REGENTS MAX
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, RoleAssignForm, LEPickerForm, StudentAssessmentForm, GradeAssessmentForm, TeacherClassForm, AssignmentOptionsForm
from app.models import User, Classroom, LE_question_bank, Assignments, StudentAssessmentResults, Classes, Students

#routes to the teacher index page
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required

def index():

	form = RoleAssignForm()
	if form.validate_on_submit():
		count = 0
		if (form.is_student.data ==True):
			count +=1
		if (form.is_teacher.data ==True):
			count +=1
		if (form.is_admin.data ==True):
			count +=1
		if (count > 1 or count ==0):
			flash("You must select an account type. You may only select one account type. Student, Teacher, or Administrator")
		else:
			if (form.is_student.data ==True):
				return redirect(url_for('studentindex'))
			if (form.is_teacher.data ==True and form.teacher_valid.data ==""):
				flash("Please enter your teacher classroom code")
			elif (form.is_teacher.data ==True and form.teacher_valid.data !='teacher'):
				flash("incorrect clasroom code")
			elif (form.is_teacher.data ==True and form.teacher_valid.data =='teacher'):
				return redirect(url_for('teacherindex'))
			if (form.is_admin.data ==True and form.admin_valid.data ==""):
				flash("Please enter your admin school code")
			elif (form.is_admin.data ==True and form.admin_valid.data !='admin'):
				flash("incorrect school code")
			elif (form.is_admin.data ==True and form.admin_valid.data =='admin'):
				return redirect("https://clinton-dash.herokuapp.com/regents-map")
				#return redirect(url_for('adminindex'))
	else:
		return render_template('index.html', title='Teacher Home', form=form)
	return render_template('index.html', title='Teacher Home', form=form)

@app.route('/teacher_index', methods=['GET', 'POST'])
@login_required


#This needs to read the database of classess and return the list of classess for a teacher
def teacherindex():
	all_data = []

	#Get all "class_name" WHERE "teacher_id" = current_user
	teacher_class=Classroom.query.filter_by(teacher_username=current_user.username).all()
	for ind_class in teacher_class:
		per_class_data = []
		per_class_data.append(ind_class.class_name)
		per_class_data.append(ind_class.student_count)
		all_data.append(per_class_data)


	print('This is all the data being passed to the html page')
	print(all_data)

	return render_template('teacher_index.html', title='Teacher Home', all_data=all_data)

#routes to the student index page
@app.route('/student_index', methods=['GET', 'POST'])
@login_required

def studentindex():
	user = {'username': 'charles'}
	#Need to return the list of student classes in the render_template
	class_list = []
	student_classes=Classes.query.filter_by(student_id=current_user.id).all()
	for each in student_classes:
		the_class_code = each.class_code
		class_info = Classroom.query.filter_by(class_code=the_class_code).first()
		class_name = class_info.class_name
		class_list.append(class_name)


	return render_template('student_index.html', title='Student Home', classes=class_list)

#Route for teachers to inspect assignments
@app.route('/inspect_assignment/<code>/<quiz_name>', methods=['GET', 'POST'])
@login_required

def inspectAssignment(code, quiz_name):
	student_roster = []

	classes=Classroom.query.filter_by(class_code=code).first()
	class_name = classes.class_name

	class_roster = Classes.query.filter_by(class_code=code).all()
	all_finished_quizzes = StudentAssessmentResults.query.filter_by(assignment_id=quiz_name).all()
	for student in class_roster:
		student_id = student.student_id
		complete = 'false'
		for each in all_finished_quizzes:
			if student_id == each.student_id:
				complete = 'true'
		student_name = Students.query.filter_by(id=student_id).first()
		first_name = student_name.first_name
		last_name = student_name.last_name
		first_n_last = []
		first_n_last.append(first_name)
		first_n_last.append(last_name)
		first_n_last.append(complete)
		first_n_last.append(student_id)
		student_roster.append(first_n_last)

	total_students = len(student_roster)
	count = 0
	for each in student_roster:
		if each[2] == 'true':
			count +=1
	finished_students = count

	print('This is the student roster')
	print(student_roster)

	return render_template('inspect_assignment.html', title='Inspect Assignment', class_info=student_roster, quiz_name=quiz_name, total=total_students, finished=finished_students, class_name=class_name)

#Route for teacher to select options for their assessments
@app.route('/assignment_options')
@login_required

def assignmentOptions():

	print('This is the destination')

	form = AssignmentOptionsForm()

	print('THESE ARE THE FORM FIELDS')
	feedback_list = []
	for field in form:
		if "feedback" in field.name:
			feedback_list.append(field)

	quiz = Assignments.query.filter_by(assignment_id='quiz1').all()
	print('This is the quiz')
	print(quiz)

	#This creates the quiz data to send to the student
	quiz_data = []
	count = 1
	for question in quiz:
		quiz_details= []
		question_picture = question.question_link
		correct_answer = question.correct_answer
		short_answer = question.short_answer
		question_standard = question.standard
		question_key_idea = question.key_idea
		question_number = count
		quiz_details.append(question_picture)
		quiz_details.append(correct_answer)
		quiz_details.append(short_answer)
		quiz_details.append(question_standard)
		quiz_details.append(question_key_idea)
		quiz_details.append(count)
		count += 1
		quiz_data.append(quiz_details)

	#Render the template
	return render_template('assignment_options.html', title='Assignment Options', quiz_data=quiz_data, form=form, feedback_list=feedback_list)

#routes to the admin index page
@app.route('/admin_index', methods=['GET', 'POST'])
@login_required

def adminindex():
	user = {'username': 'Principal Brown'}
	return render_template('admin_index.html', title='Admin Home')

#Get and post as methods allow for the route to be invoked in multiple isntances
@app.route('/login', methods=['GET', 'POST'])

def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			print('invalid username or password')
			flash('invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		#This remembers the page they were trying to go to
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', tilte='Register', form=form)

#Lazy route direct to Living Environment class for teacher
#This needs to be made into a generic "Classroom" route
@app.route('/teacher_classroom/<destination>' ,  methods=['GET', 'POST'])
def teacherClassroom(destination):
	#This is getting the class ID from the class_name table based on the classroom variable
	form=TeacherClassForm()

	class_destination = destination
	print('This is the class destination')
	print(class_destination)
	class_name= Classroom.query.filter_by(teacher_id=current_user.id, class_name=class_destination).first()
	get_name = class_name.class_id
	class_code = Classroom.query.filter_by(class_name=class_destination).first()
	code = class_code.class_code

	#This is getting the list of the assignments in the db
	assessments = Assignments.query.filter_by(teacher_id=current_user.id, class_id=get_name).distinct()
	print('This is the list of assignments in the class')

	temp = 'none'
	assessment_list = []
	for quiz in assessments:
		if quiz.assignment_id != temp:
			temp = quiz.assignment_id
			assessment_list.append(quiz.assignment_id)

	print(assessment_list)

	if request.method == 'POST':
		for field in form:
			print(field)

	print('Do I get here?')
	return render_template('teacher_classroom.html', title='Classroom', classroom=class_destination, quizzes=assessment_list, class_code=code, form=form)

#Lazy route direct to Living Environment class for student
@app.route('/student_classroom/<destination>' , methods=['GET', 'POST'])
def studentClassroom(destination):
	class_destination = destination
	class_code = Classroom.query.filter_by(class_name=class_destination).first()
	code = class_code.class_code
	assignments = Assignments.query.filter_by(class_code=code).all()

	temp = 'none'
	assessment_list = []
	for quiz in assignments:
		if quiz.assignment_id != temp:
			quiz_frame = []
			temp = quiz.assignment_id
			quiz_frame.append(quiz.assignment_id)
			is_done = StudentAssessmentResults.query.filter_by(assignment_id=quiz.assignment_id).first()
			if is_done is not None:
				quiz_frame.append('true')
			else:
				quiz_frame.append('false')
			assessment_list.append(quiz_frame)

	print(assessment_list)


	return render_template('student_classroom.html', title='Classroom', classroom=class_destination, quizzes=assessment_list)

#Lazy route direct for Living Environment Student assessment
@app.route('/student_assessment/<destination>',  methods=['GET', 'POST'])
def studentAssessment(destination):
	print('This is the destination')
	print(destination)
	form = StudentAssessmentForm()
	quiz = Assignments.query.filter_by(assignment_id=destination).all()
	print('This is the quiz')
	print(quiz)

	#This creates the quiz data to send to the student
	quiz_data = []
	for question in quiz:
		quiz_details= []
		question_picture = question.question_link
		correct_answer = question.correct_answer
		short_answer = question.short_answer
		quiz_details.append(question_picture)
		quiz_details.append(correct_answer)
		quiz_details.append(short_answer)
		quiz_data.append(quiz_details)

	response_list_prompts = []
	response_list_answers = []

	#This collects the students assessment form data
	responses=form.data
	print('THESE ARE ALL THE RESPONSE DATA IN THE FORM')
	print(responses)

	for response in responses:
		response_list_prompts.append(response)

	for field in form:
		response_list_answers.append(field.data)

	print(response_list_answers)

	combined_assessment_info = []
	multiple_choice_responses = []
	short_answer_responses = []

	#This seperates the short answer responses from the multiple choice responses
	for i in range(len(response_list_answers)):
		if i % 2 == 1:
			print( 'this is a short answer response ' + str(response_list_answers[i]))
			short_answer_responses.append(response_list_answers[i])
		else:
			print( 'this is a multiple choice response ' + str(response_list_answers[i]))
			multiple_choice_responses.append(response_list_answers[i])

	print(short_answer_responses)
	print(multiple_choice_responses)

	#This clears any of the old results from the table
	old_results = StudentAssessmentResults.query.filter_by(student_id=current_user.id).all()
	for each_result in old_results:
		db.session.delete(each_result)

	db.session.commit()

	#This helper function scores the students assessment
	quiz_length = len(quiz)
	mc_questions_count = 0
	correct_mc = 0
	question_count = 0
	quiz_mc_score = 0
	for question in quiz:
		if question.short_answer != 'yes':
			mc_questions_count +=1
			if str(question.correct_answer) == multiple_choice_responses[question_count]:
				correct_mc +=1
		question_count+=1

	quiz_mc_score = correct_mc/mc_questions_count
	print(quiz_mc_score)


	print('THESE ARE ALL THE SHORT ANSWER RESPONSES THAT WILL GET SAVED')
	print(short_answer_responses)
	#This adds the students new assessment results to the database
	if request.method == 'POST':
		question_count = 0
		for question in quiz:
			print('These are the individual questions')
			print(question)
			question_result = StudentAssessmentResults(student_id=current_user.id, assignment_id=question.assignment_id, question_id=question.question_id, correct_answer=question.correct_answer, student_answer=multiple_choice_responses[question_count], student_justification=short_answer_responses[question_count], assessment_score=quiz_mc_score, standard=question.standard, key_idea=question.key_idea, question_desc=question.question_description, question_link=question.question_link)
			question_count += 1
			db.session.add(question_result)

		print(len(quiz))
		db.session.commit()


	print('This is the quiz sent to the student')
	print(quiz_data)

	#This redirects student to the results page after submission
	if request.method == 'POST':
		print('Hello testing!!!')
		return redirect(url_for('assessmentResults', quiz_name=destination, user=current_user))

	#Render the template
	return render_template('student_assessment.html', title='Student Assessment', assessment='thistest', form=form, details=quiz_data)


#This is the route that allows a teacher to grade a student assessment
@app.route('/grade_assignment/<quiz_name>/<user>', methods=['GET', 'POST'])
def gradeAssignment(quiz_name, user):

	print('THIS IS THE USER')
	print(user)
	student = Students.query.filter_by(id=user).first()
	full_name = (student.first_name + student.last_name)
	quiz_name= quiz_name

	class_sql = Assignments.query.filter_by(assignment_id=quiz_name).first()
	class_code = class_sql.class_code

	form =GradeAssessmentForm()


	feedback_responses = []
	for field in form:
		feedback_responses.append(field.data)



	print('THIS IS THE FEEDBACK RESPONSES')
	print(feedback_responses)


	form_list = []
	form_field_list = []
	for i in range(10):
		item = 'form.feedback' + str(i + 1) + '()'
		form_list.append(item)

	print('this is the form_list')
	print(form_list)

	for field in form:
		form_field_list.append(field)

	print('this is the form_field_list')
	print(form_field_list)


	quiz = Assignments.query.filter_by(assignment_id=quiz_name).all()

	#These are the results from the specific quiz
	quiz_results = StudentAssessmentResults.query.filter_by(student_id=user, assignment_id=quiz_name).all()
	result_array = []
	for question in quiz_results:
		question_array = []
		correct_answer = question.correct_answer
		student_answer = question.student_answer
		justification = question.student_justification
		mc_score = question.assessment_score
		teacher_feedback = question.teacher_feedback
		question_array.append(correct_answer)
		question_array.append(student_answer)
		question_array.append(justification)
		question_array.append(mc_score)
		question_array.append(teacher_feedback)
		result_array.append(question_array)

	#This creates the quiz data to send to the student
	quiz_data_array = []
	for question in quiz:
		quiz_details= []
		question_picture = question.question_link
		correct_answer = question.correct_answer
		short_answer = question.short_answer
		quiz_details.append(question_picture)
		quiz_details.append(correct_answer)
		quiz_details.append(short_answer)
		quiz_data_array.append(quiz_details)

	print('THESE ARE THE RESULTS')
	print(result_array)

	student_quiz = StudentAssessmentResults.query.filter_by(student_id=user, assignment_id=quiz_name).all()

	#Need to Add feedback to the specific student quiz
	if request.method == 'POST':
		count = 0
		for question in student_quiz:
			question.teacher_feedback = feedback_responses[count]
			count += 1
			db.session.commit()
		return redirect(url_for('inspectAssignment', code=class_code ,quiz_name=quiz_name))




	return render_template('grade_assignment.html', title='Grade Assessment', details=quiz_data_array, results=result_array, form_field_list=form_field_list, form=form, full_name=full_name, quiz_name=quiz_name)

#This is the redirect page for the student assessment results
@app.route('/assessment_results/<quiz_name>/<user>', methods=['GET', 'POST'])
def assessmentResults(quiz_name, user):
	print(request.args.get('quiz_name'))

	quiz = Assignments.query.filter_by(assignment_id=quiz_name).all()
	print('Here is the quiz')
	print(quiz)

	#These are the results from the specific quiz
	quiz_results = StudentAssessmentResults.query.filter_by(student_id=current_user.id, assignment_id=quiz_name).all()
	result_array = []
	for question in quiz_results:
		question_array = []
		correct_answer = question.correct_answer
		student_answer = question.student_answer
		justification = question.student_justification
		teacher_feedback = question.teacher_feedback
		mc_score = question.assessment_score
		question_array.append(correct_answer)
		question_array.append(student_answer)
		question_array.append(justification)
		question_array.append(mc_score)
		question_array.append(teacher_feedback)
		result_array.append(question_array)

	print('THIS IS THE RESULT ARRAY THAT SHOULD CONTAIN 8, 9, 10')
	print(quiz_results)

	#This creates the quiz data to send to the student
	quiz_data_array = []
	for question in quiz:
		quiz_details= []
		question_picture = question.question_link
		correct_answer = question.correct_answer
		short_answer = question.short_answer
		quiz_details.append(question_picture)
		quiz_details.append(correct_answer)
		quiz_details.append(short_answer)
		quiz_data_array.append(quiz_details)

	print('Here is the quiz data array')
	print(quiz_data_array)

	return render_template('assessment_results.html', title='Assessment Results', details=quiz_data_array, results=result_array)


@app.route('/create_assignment', methods=['GET', 'POST'])
def createAssignment():
	#Need to inspect all the form data and find out which boxes were checked
	#If a box was checked, a query needs to be made that includes that key idea
	form = LEPickerForm()
	true_box_labels=[]
	lab_results =[]
	standard_results=[]

	lab_numbers =[]
	standard_numbers=[]

	lab_links = []
	standard_links = []

	for field in form:
		#print(field.name)
		#print(field.data)
		if "s1" in field.name:
			if field.data ==True:
				standard_results.append(field.name)
		elif "s4" in field.name:
			if field.data ==True:
				standard_results.append(field.name)
		elif "l" in field.name:
			if field.data ==True:
				lab_results.append(field.name)

	for result in lab_results:
		numberfy = ''.join(x for x in result if x.isdigit())
		lab_numbers.append(numberfy)

	for result in standard_results:
		numberfy = str(''.join(x for x in result if x.isdigit()))
		own_list = []
		own_list.append(int(numberfy[0]))
		own_list.append(int(numberfy[1]))
		standard_numbers.append(own_list)

	#this is the query and operation that pulls lab image links
	lab_questions= [LE_question_bank.query.filter_by(lab=lab_num).all() for lab_num in lab_numbers]
	#print (lab_questions)

	if len(lab_questions) > 0:
		the_lab_list = lab_questions[0]
		for ind_question in the_lab_list:
			details = []
			details.append(ind_question.question_link)
			details.append(ind_question.lab)
			lab_links.append(deatils)
			#print(ind_question.question_link)

	#This is the query and operation that pulls standard image lab_links
	standard_questions= [LE_question_bank.query.filter_by(standard=standard_num[0], key_idea=standard_num[1]).all() for standard_num in standard_numbers]
	#print (standard_questions)

	if len(standard_questions) > 0:
		for sublist in standard_questions:
			for ind_question in sublist:
				details = []
				details.append(ind_question.question_link)
				details.append(ind_question.standard)
				details.append(ind_question.key_idea)
				standard_links.append(details)
				#print(ind_question.question_link)

	print('THESE ARE THE STANDARD LINKS')
	print(standard_links)

	return render_template('create_assignment.html', title='Create Assignment', form=form, lab_results=lab_links, standard_results=standard_links)

#Route for student form on Bootstrap next_page
