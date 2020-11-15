# package imports
import collections

from HomePhilosopher.Api_Connector.API_KEYS import Crime_API_KEY, Zillow_API_KEY, Rapid_API_KEY, Climate_API_KEY, \
    Google_API_KEY
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
    return json_source


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
def get_crime_statistics(county, state_code):
    with open('county_json.json', 'r') as f:
        county_json = f.read()
        county_json = json.loads(county_json)

    county = county.lower()
    state_code = state_code.lower()
    json_key = '{}{}'.format(county, state_code)
    ori_list = county_json.get(json_key, None)

    if not ori_list:
        raise Exception('County {} Is Not Found'.format(county))

    ori_list = ori_list['ori']

    offense = 'rape'
    variable = 'count'

    url = 'https://api.usa.gov/crime/fbi/sapi/api/data/nibrs/{offense}/offender/agencies/{ori}/{variable}?api_key={api_key}'

    year_data = {}
    for ori in ori_list:
        session = requests.session()
        response = session.get(url=url.format(api_key=Crime_API_KEY,
                                              offense=offense,
                                              ori=ori,
                                              variable=variable))
        if response.status_code != 200:
            raise Exception('Crime Invalid Status Code: {}'.format(response.status_code))

        json_source = json.loads(response.content)

        results = json_source.get('results', [])

        for data in results:
            if data['data_year'] in year_data:
                year_data[data['data_year']] += data['count']
            else:
                year_data[data['data_year']] = data['count']

    for year in range(2000, 2020):
        if year not in year_data:
            year_data[year] = 0

    year_data = collections.OrderedDict(sorted(year_data.items()))

    crime_data = {'county': county, 'offense': offense, 'variable': variable, 'year_data': year_data}

    print(json.dumps(crime_data))
    return year_data

# create county dictionary json that can be referred to by the crime statistics
def create_county_dictionary():
    agency_json = get_agencies()
    county_json = {}

    for key, state_item in agency_json.items():
        for state_key, agency_item in state_item.items():
            county_name = agency_item['county_name'].lower()
            state_abbr = agency_item['state_abbr'].lower()
            latitude = agency_item['latitude']
            longitude = agency_item['longitude']
            county_key = agency_item['ori']

            json_key = '{}{}'.format(county_name, state_abbr)
            if json_key in county_json:
                county_json[json_key]["ori"].append(county_key)
            else:
                county_json[json_key] = {}
                county_json[json_key]["ori"] = [county_key]
                county_json[json_key]["latitude"] = latitude
                county_json[json_key]["longitude"] = longitude

    with open('county_json.json', 'w') as f:
        f.write(json.dumps(county_json, indent=4))


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
        "x-rapidapi-key": Rapid_API_KEY,
        'content-type': "application/x-www-form-urlencoded"
    }
    response = session.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        raise Exception('Zillow Invalid Status Code: {}'.format(response.status_code))
    print(response.text)


# climate information (precipitation radar)
def get_climate_information(lat, long):
    url = 'https://app.climate.azavea.com/api/city/nearest?lat={lat}&lon={lon}'.format(lat=lat, lon=long)

    headers = {
        'Authorization': 'Token {}'.format(Climate_API_KEY)
    }

    session = requests.session()
    response = session.get(url=url, headers=headers)

    if response.status_code != 200:
        raise Exception('Climate Invalid Status Code: {}'.format(response.status_code))

    city = json.loads(response.content)
    city = city['features'][0]['id']

    if not city:
        raise Exception('Climate Location ID Not Found')

    # scenario is RCP85 or historical
    url = "https://app.climate.azavea.com/api/climate-data/{city}/{scenario}?variables=pr&years=2010%3A2020&agg=avg"
    url = url.format(city=city, scenario='RCP85')

    response = session.get(url=url, headers=headers)

    if response.status_code != 200:
        raise Exception('Climate Invalid Status Code: {}'.format(response.status_code))

    climate_source = json.loads(response.content)
    year_data = {}

    if 'data' not in climate_source:
        raise Exception('Data Not Found For {}/{}'.format(lat, long))

    climate_data = climate_source['data']
    for year in climate_data:
        year_sum = 0.0
        for pr in climate_data[year]['pr']:
            if pr:
                year_sum += float(pr)
        year_data[year] = year_sum

    print(year_data)
    return year_data


# get the zip code from lat long; https://www.bigdatacloud.com/geocoding-apis/free-reverse-geocode-to-city-api
def get_zip_code(lat, lon):
    url = 'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en'
    url = url.format(lat=lat, lon=lon)

    session = requests.session()
    response = session.get(url=url)

    if response.status_code != 200:
        raise Exception('Climate Invalid Status Code: {}'.format(response.status_code))

    zip_source = json.loads(response.content)

    zip_code = zip_source['postcode']

    return zip_code


def create_environmental_json(fips_code):
    with open('environment_json.txt', 'r') as f:
        environment_json = f.read()
        environment_json = json.loads(environment_json)

    for key, value in environment_json:
        print(value)
        break
