from flask import *
import pandas as pd
import random
import MySQLdb
import util
#import lol_classifier




MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_DB = 'Hackru'
MYSQL_PASSWORD = 'Nitro06snow'
app = Flask(__name__)
# mysql = MySQL(app)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_DB'] = 'Hackru'
# app.config['MYSQL_PASSWORD'] = 'Nitro06snow'

mydb = MySQLdb.connect(host=MYSQL_HOST,
	user=MYSQL_USER,
	passwd=MYSQL_PASSWORD,
	db=MYSQL_DB,use_unicode=True, charset="utf8")

@app.route('/login')
def login_page():
	return app.send_static_file('Login.html')

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
