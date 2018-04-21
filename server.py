from flask import *
from flask_mysqldb import MySQL
import pandas as pd
import random
import util
#import lol_classifier


app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'Hackru'
app.config['MYSQL_PASSWORD'] = 'Nitro06snow'


@app.route('/')
def index():
	return render_template('index.html')

#@app.route('/filter')
#def applicant_filter():


#@app.route('/viewer'):
#def applicant_viewer


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
