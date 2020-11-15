# package imports
import collections

# base imports
import requests
import json
import pandas as pd

from countymapperapp import API_KEYS as KEYS

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
    response = session.get(url=url.format(api_key=KEYS.Crime_API_KEY))
    if response.status_code != 200:
        raise Exception('Agency Invalid Status Code: {}'.format(response.status_code))

    json_source = json.loads(response.content)
    with open('countymapperapp\\agencies.json', 'w') as f:
        f.write(json.dumps(json_source, indent=4))
    return json_source


'''
Data From:
    https://crime-data-explorer.fr.cloud.gov/api

Parameters:
    ori -> Ori Code
    offense -> The crime that has been offended (76 options)
    variable -> the format of data (age, count ethnicity, race, sex)

Offenses:
    Offenses to input:aggravated-assault,all-other-larceny,all-other-offenses,animal-cruelty,arson,assisting-or-promoting-prostitution,bad-checks,betting,bribery,burglary-breaking-and-entering,counterfeiting-forgery,credit-card-automated-teller-machine-fraud,destruction-damage-vandalism-of-property,driving-under-the-influence,drug-equipment-violations,drug-violations,drunkenness,embezzlement,extortion-blackmail,false-pretenses-swindle-confidence-game,fondling,gambling-equipment-violation,hacking-computer-invasion,human-trafficking-commerical-sex-acts,human-trafficking-commerical-involuntary-servitude,identity-theft,impersonation,incest,intimidation,justifiable-homicide,kidnapping-abduction,motor-vehicle-theft,murder-and-nonnegligent-manslaughter,negligent-manslaughter,operating-promoting-assiting-gambling,curfew-loitering-vagrancy-violations,peeping-tom,pocket-picking,pornography-obscence-material,prostitution,purchasing-prostitution,purse-snatching,rape,robbery,sexual-assult-with-an-object,sex-offenses-non-forcible,shoplifting,simple-assault,sodomy,sports-tampering,statutory-rape,stolen-property-offenses,theft-from-building,theft-from-coin-operated-machine-or-device,theft-from-motor-vehicle,theft-of-motor-vehicle-parts-or-accessories,theft-from-motor-vehicle,weapon-law-violation,welfare-fraud,wire-fraud,not-specified,liquor-law-violations,crime-against-person,crime-against-property,crime-against-society,assault-offenses,homicide-offenses,human-trafficking-offenses,sex-offenses,sex-offenses-non-forcible, fraud-offenses,larceny-theft-offenses, drugs-narcotic-offenses,gambling-offenses,prostitution-offenses,all-offenses
'''
# TODO: Expand Out instead of these small agencies, combine all of the values for the agencies into a county and then
# use those values instead. Relate County name to list of ori codes
def get_crime_statistics(county_state_list, offenses=None):
    if not offenses:
        offenses = ['aggravated-assault', 'drug-violations', 'drunkenness', 'arson', 'bribery', 'rape']
    if not isinstance(offenses, list):
        offenses = [offenses]
    crime_data = {}
    for offense in offenses:
        crime_data[offense] = {}
        for county, state_code in county_state_list:
            with open('countymapperapp\\county_json.json', 'r') as f:
                county_json = f.read()
                county_json = json.loads(county_json)

            county = county.lower()
            state_code = state_code.lower()
            json_key = '{}{}'.format(county, state_code)
            ori_list = county_json.get(json_key, None)

            if not ori_list:
                raise Exception('County {} Is Not Found'.format(county))

            ori_list = ori_list['ori']

            variable = 'count'

            url = 'https://api.usa.gov/crime/fbi/sapi/api/data/nibrs/{offense}/offender/agencies/{ori}/{variable}?api_key={api_key}'

            year_data = {}
            for ori in ori_list:
                session = requests.session()
                response = session.get(url=url.format(api_key=KEYS.Crime_API_KEY,
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

            year_data = collections.OrderedDict(sorted(year_data.items(), reverse=True))

            data = {'county': county, 'offense': offense, 'variable': variable, 'year_data': year_data}
            crime_data[offense][(county, state_code)] = data

    return crime_data

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

    with open('countymapperapp\\county_json.json', 'w') as f:
        f.write(json.dumps(county_json, indent=4))


# method used to communicate with zillow api
# TODO: current doesn't work as we don't have access to zillow api for house sellings
def get_address_information(address, zip_code):
    session = requests.session()
    url = "https://zillowdimashirokovv1.p.rapidapi.com/GetSearchResults.htm"
    payload = "rentzestimate=true&rentzestimate=false&zws-id={zillow_key}&citystatezip={zip}&address={address}"
    payload = payload.format(zillow_key=KEYS.Zillow_API_KEY,
                             address=address.replace(' ', '%20'),
                             zip=zip_code)
    headers = {
        'x-rapidapi-host': "ZillowdimashirokovV1.p.rapidapi.com",
        "x-rapidapi-key": KEYS.Rapid_API_KEY,
        'content-type': "application/x-www-form-urlencoded"
    }
    response = session.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        raise Exception('Zillow Invalid Status Code: {}'.format(response.status_code))


# climate information (precipitation radar), returns none if
def get_climate_information(county_state_list):
    with open('countymapperapp\\county_json.json', 'r') as f:
        county_source = json.loads(f.read())

    climate_data = {}
    for county, state_code in county_state_list:
        key = '{}{}'.format(county.lower(), state_code.lower())
        lat = county_source[key]['latitude']
        long = county_source[key]['longitude']

        url = 'https://app.climate.azavea.com/api/city/nearest?lat={lat}&lon={lon}'.format(lat=lat, lon=long)

        headers = {
            'Authorization': 'Token {}'.format(KEYS.Climate_API_KEY)
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

        precip_data = climate_source['data']
        for year in precip_data:
            year_sum = 0.0
            for pr in precip_data[year]['pr']:
                if pr:
                    year_sum += float(pr)
            year_data[year] = year_sum

        climate_data[(county, state_code)] = year_data

    for key, item in climate_data.items():
        for year in range(2010, 2021):
            if str(year) not in item:
                climate_data[key][str(year)] = 0

    return climate_data


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


# environmental api
def create_environmental_json(fips_codes):
    df = pd.read_csv('countymapperapp\\pollution_data.csv')

    env_json = {}
    for fips in fips_codes:
        state_code = int(fips[:2])
        county_code = int(fips[2:])
        env_json[fips] = {}
        for index, row in df.iterrows():
            if int(row['State Code']) == state_code and int(row['County Code']) == county_code:
                parameter = row['Parameter Name']
                units = row['Units of Measure']
                mean = row['Arithmetic Mean']

                if parameter in env_json:
                    env_json[fips][parameter]['mean'].append(mean)
                else:
                    env_json[fips][parameter] = {}
                    env_json[fips][parameter]['mean'] = [mean]
                    env_json[fips][parameter]['units'] = units

        if not env_json[fips]:
            county_code = None
            for index, row in df.iterrows():
                if int(row['State Code']) == state_code:
                    if not county_code or int(row['County Code']) == county_code:
                        county_code = int(row['County Code'])
                        parameter = row['Parameter Name']
                        units = row['Units of Measure']
                        mean = row['Arithmetic Mean']

                        if parameter not in env_json:
                            env_json[fips][parameter] = {}
                            env_json[fips][parameter]['mean'] = mean
                            env_json[fips][parameter]['units'] = units

    return env_json
