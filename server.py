from flask import *
import pandas as pd
import random
import MySQLdb
import util
import flask_login
import pickle
import MySQLdb.cursors




MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_DB = 'Hackru'
MYSQL_PASSWORD = 'Nitro06snow'

jobDB = {}
jobDB_File = 'jobDB.pickle'

mydb = MySQLdb.connect(host=MYSQL_HOST,
	user=MYSQL_USER,
	passwd=MYSQL_PASSWORD,
	db=MYSQL_DB,use_unicode=True, charset="utf8",
	cursorclass=MySQLdb.cursors.DictCursor)

app = Flask(__name__)
app.secret_key = 'ej&e2gw*^e0i_&_0^ws)yk)d$th!kz2zd&0rx=syf6s8+p-r3q'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
	pass

def update(id):
	major = jobDB[id][2]
	skill = jobDB[id][3]
	print("update {}".format(id))
	cursor = mydb.cursor()
	if not major and not skill:
		sql = "select distinct * from applicants"
		cursor.execute(sql)
	elif major and not skill:
		sql = "select distinct applicants.* from applicants, applicantEdu where applicant.id = applicantEdu.id and applicantEdu.major = %s"
		values = (major,)
		cursor.execute(sql, values)
	elif not major and skill:
		sql = "select distinct applicants.* from applicants, applicantSkill where applicant.id = applicantSkill.id and applicantSkill.name = %s"
		values = (skill,)
		cursor.execute(sql, values)
	else:
		sql = "select distinct applicants.* from applicants, applicantSkill, applicantEdu where applicant.id = applicantSkill.id and applicant.id = applicantEdu.id and applicantSkill.name = %s and applicantEdu.major = %s"
		values = (skill,major)
		cursor.execute(sql, values)
	rv = cursor.fetchall()
	for applicant in rv:
		print(applicant)
		sql = "select School, degree, major, gradDate, GPA from applicantEdu where id = %s"
		values = (applicant['id'],)
		cursor.execute(sql, values)
		eduRv = cursor.fetchall()
		applicant['education'] = []
		for education in eduRv:
			applicant['education'].append(education)
		sql = "select name from applicantSkill where id = %s"
		value = (applicant['id'],)
		cursor.execute(sql, values)
		skRv = cursor.fetchall()
		applicant['skills'] = []
		for skill in skRv:
			applicant['skills'].append(skill)
		applicant = json.dumps(applicant)
		if not applicant in jobDB[id][0]:
			jobDB[id][0].append(applicant)
		else:
			continue
	with open(jobDB_File, 'wb') as f:
		pickle.dump(jobDB, f)


@login_manager.user_loader
def load_user(user_id):
	sql = 'SELECT id, email FROM users WHERE id = %s'
	cursor = mydb.cursor()
	cursor.execute(sql, (user_id,))
	if len(list(cursor)) > 0:
		user = User()
		user.id = user_id
		return user
	return None

@app.route('/login', methods=['GET', 'POST'])
def login_page():
	if request.method == 'GET':
		return app.send_static_file('Login.html')

	sql = 'SELECT id, email, password FROM users WHERE email = %s'
	cursor = mydb.cursor()
	cursor.execute(sql, (request.form['email'],))
	if len(list(cursor)) > 0:
		db_pass = list(cursor)[0][2]
		if db_pass == request.form['password']:
			user = User()
			user.id = list(cursor)[0][0]
			flask_login.login_user(user)
			return redirect('/dashboard')

	#fail
	return app.send_static_file('Login.html')

@app.route('/logout')
@flask_login.login_required
def logout():
	flask_login.logout_user()
	return redirect('/')


@app.route('/signup', methods = ['GET', 'POST'])
def create_user():
	if request.method == 'GET':
		return app.send_static_file('Signup.html')
	elif request.method ==  'POST':
		cursor = mydb.cursor()
		data = request.form
		print(data)
		sql = "INSERT INTO users (email, password, compOrApp) VALUES (%s,%s,%s)"
		values = (data['email'],data['password'],data['compOrApp'])
		cursor.execute(sql, values)
		mydb.commit()
		cursor.close()
		if int(data['compOrApp']) is 0:
			id = cursor.lastrowid
			return redirect("/create_job")
		else:
			return redirect("/create_app")
	else:
		print("BAD NEWS")


@app.route('/make_job', methods = ['GET','POST'])
def create_job():
	if request.method == 'GET':
		return app.send_static_file('jobPost.html')
	elif request.method ==  'POST':
		cursor = mydb.cursor()
		data = request.form
		print(data)
		sql = "INSERT INTO jobs (companyId, companyName, title, description, email, location_country, location_state, location_city) VALUES (%s,%s,%s, %s, %s, %s, %s, %s)"
		values = (flask_login.current_user.get_id(), data['companyName'], data['title'], data['description'], data['email'], data['location_country'], data['location_state'], data['location_city'])
		cursor.execute(sql, values)
		id = cursor.lastrowid
		sql = "INSERT INTO jobFilters (jobId, major, skill) VALUES (%s,%s,%s)"
		values = (id, data['major'], data['skill'])
		cursor.execute(sql, values)
		mydb.commit()
		cursor.close()
		jobDB[id] = [[], 0, data['major'], data['skill']]

		return redirect(url_for('.applicant_viewer', job_id = id))
	else:
		print("BAD NEWS")


@app.route('/')
def index():
	return render_template('')

#@app.route('/filter')
#def applicant_filter():


@app.route('/viewer/<job_id>',methods = ['GET'])
def applicant_viewer(job_id):
	job_id = int(job_id)
	update(job_id)
	cur = jobDB[job_id][0][jobDB[job_id][1]]
	jobDB[job_id][1] += 1
	return render_template("viewer.html")



@app.route('/viewer/<job_id>/<applicant_id>', methods = ['POST'])
def applicant_viewer_swipe_confirm(job_id,applicant_id):
		print(job_id, applicant_id)

if __name__ == '__main__':
	with open(jobDB_File, 'rb') as f:
		jobDB = pickle.load(f)
	app.run(debug=True, host='0.0.0.0')
