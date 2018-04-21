import requests

ICIMS_API_KEY = '$2a$12$Kp8l3eJW3GVGaCOlBqY1j.s6O4fRU21c7P29p4KbuSRAztb9JU2Ee'
ICIMS_HEADER = {'Authorization': 'Bearer {}'.format(ICIMS_API_KEY)}
ICIMS_COMPANY = 2040
ICIMS_BASE_URL = 'https://hackicims.com/api/v1/companies/{}/'.format(ICIMS_COMPANY)

def get_jobs():
    return requests.get(ICIMS_BASE_URL + 'jobs', headers=ICIMS_HEADER).json()

def get_people():
    return requests.get(ICIMS_BASE_URL + 'people', headers=ICIMS_HEADER).json()