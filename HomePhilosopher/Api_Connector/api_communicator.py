# package imports
from HomePhilosopher.Api_Connector.API_KEYS import Crime_API_KEY, Zillow_API_KEY
# base imports
import requests
import json

'''
Python File that will be used to communicate with the API's
    The API keys for ones that need it will be held in API_KEYS.py

Crime Api - https://github.com/fbi-cde/crime-data-frontend
    Crime_API_KEY


'''




# method used to get the agency listings and then put them in a json file
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
Data From:
    https://crime-data-explorer.fr.cloud.gov/api

Parameters:
    ori -> Ori Code
    offense -> The crime that has been offended (76 options)
    variable -> the format of data (age, count ethnicity, race, sex)
'''
# TODO: Expand Out instead of these small agencies, combine all of the values for the agencies into a county and then
# use those values instead. Relate County name to list of ori codes
def get_crime_statistics(ori, offense, variable='count'):
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


# method used to communicate with zillow api
# TODO: current doesn't work as we don't have access to zillow api for house sellings
def get_address_information(address, zip_code):
    session = requests.session()
    url = "https://zillowdimashirokovv1.p.rapidapi.com/GetSearchResults.htm"
    payload = "rentzestimate=true&rentzestimate=false&zws-id={zillow_key}&citystatezip={zip}&address={address}"
    payload = payload.format(zillow_key=Zillow_API_KEY,
                             address=address.replace(' ', '%20'),
                             zip=zip_code)
    headers = {
        'x-rapidapi-host': "ZillowdimashirokovV1.p.rapidapi.com",
        "x-rapidapi-key": "e1b68dbd4dmsh95223875a4844b0p14cd58jsn1829f0968cc2",
        'content-type': "application/x-www-form-urlencoded"
    }
    response = session.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        raise Exception('Zillow Invalid Status Code: {}'.format(response.status_code))
    print(response.text)
