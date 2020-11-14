# package imports
from HomePhilosopher.Api_Connector.API_KEYS import Crime_API_KEY
# base imports
import requests
import json

'''
Python File that will be used to communicate with the API's
    The API keys for ones that need it will be held in API_KEYS.py

Crime Api - https://github.com/fbi-cde/crime-data-frontend
    Crime_API_KEY


'''


def get_agencies():
    url = 'https://api.usa.gov/crime/fbi/sapi/api/agencies?api_key={api_key}'
    session = requests.session()
    response = session.get(url=url.format(api_key=Crime_API_KEY))
    if response.status_code != 200:
        raise Exception('Agency Invalid Status Code: {}'.format(response.status_code))

    json_source = json.loads(response.content)
    with open('agencies.json', 'w') as f:
        f.write(json.dumps(json_source, indent=4))


'''
TODO: Expand Out instead of these small agencies, combine all of the values for the agencies into a county and then
use those values instead. Relate County name to list of ori codes
Data From:
    https://crime-data-explorer.fr.cloud.gov/api

Parameters:
    ori -> Ori Code
    offense -> The crime that has been offended (76 options)
    variable -> the format of data (age, count ethnicity, race, sex)
'''
def get_crime_statistics(ori='OH0186100', offense='rape', variable='count'):
    with open('agencies.json', 'r') as f:
        agency_json = f.read()
    agency_json = json.loads(agency_json)
    state_code = ori[:2]
    county = agency_json[state_code][ori]['county_name']
    state = agency_json[state_code][ori]['state_name']
    url = 'https://api.usa.gov/crime/fbi/sapi/api/data/nibrs/{offense}/offender/agencies/{ori}/{variable}?api_key={api_key}'

    session = requests.session()
    response = session.get(url=url.format(api_key=Crime_API_KEY,
                                          offense=offense,
                                          ori=ori,
                                          variable=variable))
    if response.status_code != 200:
        raise Exception('Crime Invalid Status Code: {}'.format(response.status_code))

    json_source = json.loads(response.content)

    results = json_source['results']

    data_counts = []
    for data in results:
        data_counts.append((data['data_year'], data['count']))

    print((county, state))
    print(data_counts)
