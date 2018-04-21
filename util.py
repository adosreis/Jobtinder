import requests
import csv
import MySQLdb
import random


MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_DB = 'Hackru'
MYSQL_PASSWORD = 'Nitro06snow'

ICIMS_API_KEY = '$2a$12$Kp8l3eJW3GVGaCOlBqY1j.s6O4fRU21c7P29p4KbuSRAztb9JU2Ee'
ICIMS_HEADER = {'Authorization': 'Bearer {}'.format(ICIMS_API_KEY)}
ICIMS_COMPANY = 2046
ICIMS_BASE_URL = 'https://hackicims.com/api/v1/companies/{}/'.format(ICIMS_COMPANY)

def get_jobs():
    try:
        return requests.get(ICIMS_BASE_URL + 'jobs', headers=ICIMS_HEADER).json()
    except HTTPError as err:
        if err.response.status_code == 404:
            print('api request not found error')
        else:
            print('unknown error occured')
        return None


def get_people():
    try:
        print("get_people")
        return requests.get(ICIMS_BASE_URL + 'people', headers=ICIMS_HEADER).json()
    except HTTPError as err:
        if err.response.status_code == 404:
            print('api request not found error')
        else:
            print('unknown error occured')
        return None


def applicant_upload(json):
    print("starting upload")
    mydb = MySQLdb.connect(host=MYSQL_HOST,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWORD,
        db=MYSQL_DB,use_unicode=True, charset="utf8")
    cursor = mydb.cursor()
    applicants = []
    for applicant in json:
        print(applicant['id'])
        try:
            if not applicant['id'] in applicant:
                applicants.append(applicant['id'])
                address = applicant['address']
                address_country = address['country']
                address_state = address['state']
                address_city = address['city']
                sqlApp = "INSERT INTO applicants (id, email, firstName, lastName, address_country, address_state, address_city) VALUES (%s,%s,%s,%s,%s,%s,%s)"

                valuesApp = (applicant['id'],applicant['email'],applicant['firstName'],applicant['lastName'],address_country, address_state, address_city)
                #print(valuesApp)
                cursor.execute(sqlApp, valuesApp)
                for edu in applicant['education']:
                    school = edu['school']
                    degree = edu['degree']
                    major = edu['major']
                    gradDate = edu['graduationDate']
                    gpa = round(random.uniform(2.5,4.0), 2)
                    sqlEdu = "INSERT INTO applicantEdu (id, school, degree, major, gradDate, GPA) VALUES (%s,%s,%s,%s,%s,%s)"
                    valuesEdu = (applicant['id'],school, degree, major, gradDate, gpa)
                    #print(valuesEdu)
                    cursor.execute(sqlEdu, valuesEdu)
                for skill in applicant['skills']:
                    name = skill['name']
                    sqlSkills = "INSERT INTO applicantSkill (id, name) VALUES (%s,%s)"
                    valuesSk = (applicant['id'],name)
                    #print(valuesSk)
                    cursor.execute(sqlSkills, valuesSk)
            else:
                continue
        except:
            print("stupid name")
            continue

    #close the connection to the database.
    mydb.commit()
    cursor.close()

if __name__ == '__main__':
    people = get_people()
    applicant_upload(people)
    #(id, email,firstName, lastName, address_country, address_state, address_city)
    #(id, school, degree, major, gradDate, GPA)
    #(id, skill)
