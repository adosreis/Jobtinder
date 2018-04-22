from flask import *
import pandas as pd
import random
import MySQLdb
import util
#import lol_classifier

import flask_login




MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_DB = 'Hackru'
MYSQL_PASSWORD = 'Nitro06snow'
# mysql = MySQL(app)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_DB'] = 'Hackru'
# app.config['MYSQL_PASSWORD'] = 'Nitro06snow'

mydb = MySQLdb.connect(host=MYSQL_HOST,
	user=MYSQL_USER,
	passwd=MYSQL_PASSWORD,
	db=MYSQL_DB,use_unicode=True, charset="utf8")

app = Flask(__name__)
app.secret_key = 'ej&e2gw*^e0i_&_0^ws)yk)d$th!kz2zd&0rx=syf6s8+p-r3q'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
	pass

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
			return redirect(url_for('.create_comp', compId = id))
		else:
			return redirect("/create_app", code=302)
	else:
		print("BAD NEWS")


@app.route('/create_comp', methods = ['GET','POST'])
def create_comp(compId):
	if request.method == 'GET':
		return app.send_static_file('jobPost.html')
	elif request.method ==  'POST':
		cursor = mydb.cursor()
		data = request.form
		print(data)
		sql = "INSERT INTO jobs (companyId, companyName, title, description, email, location_country, location_state, location_city) VALUES (%s,%s,%s, %s, %s, %s, %s, %s)"
		values = (data['companyId'], data['companyName'], data['title'], data['description'], data['email'], data['location_country'], data['location_state'], data['location_city'])
		cursor.execute(sql, values)
		mydb.commit()
		cursor.close()
		id = cursor.lastrowid
		return redirect(url_for('.applicant_viewer', job_id = id))
	else:
		print("BAD NEWS")


@app.route('/')
def index():
	return render_template('')

#@app.route('/filter')
#def applicant_filter():


@app.route('/viewer/<job_id>',)
def applicant_viewer(job_id):
		print(job_id)


@app.route('/viewer/<job_id>/<applicant_id>', methods = ['POST'])
def applicant_viewer_swipe_confirm(job_id,applicant_id):
		print(job_id, applicant_id)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
