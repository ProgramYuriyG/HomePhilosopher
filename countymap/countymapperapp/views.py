from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.template.context_processors import csrf

from .models import *
from . import api_communicator as api_com
import json

# base index page
def index(request):
    return redirect('homepage')

# county mapper page
def county_mapper(request):
    if request.method == 'POST':
        pb = ParseBatch()
        pb.status = 1
        pb.save()

        county_names = request.POST.get('county_names').strip('; ')
        fips_ids = request.POST.get('fips_ids').strip('; ')

        county_names = county_names.split("; ")
        fips_ids = fips_ids.split("; ")

        county = [cn.split(',')[0].strip() for cn in county_names]
        state = [cn.split(',')[-1].strip() for cn in county_names]

        get_crime_stats(tuple(zip(county, state)), pb)

        offense_objects = Offense.objects.filter(run=pb)
        offense_types = list(set([o.name for o in offense_objects]))

        get_climate_stats(tuple(zip(county, state)), pb)
        climate_objects = Precipitation.objects.filter(run=pb)

        get_environmental_data(fips_ids, pb)
        environment_objects = Pollutant.objects.filter(run=pb)

        context = {'county_names': county_names,
                   'fips_ids': fips_ids,
                   'offense_types': offense_types,
                   'offense_objects': offense_objects,
                   'climate_objects': climate_objects,
                   'environment_objects': environment_objects,
                   }
        context.update(csrf(request))
        return render_to_response('county_details.html', context, RequestContext(request))
    return render(request, 'county_mapper.html')

# homepage that the user will see on page arrival
def homepage(request):
    return render(request, 'homepage.html')

# method to get the crime_stats
def get_crime_stats(count_state_list, pb):
    crime_stats = api_com.get_crime_statistics(count_state_list, None)

    for offense, counties in crime_stats.items():
        for key, data in counties.items():
            crime_count = 0
            year_data = 0
            for year_key, value in data['year_data'].items():
                crime_count += 1
                if crime_count > 5:
                    break
                year_data += int(value)
            county = key[0]
            state = key[1]

            of_res = Offense()
            of_res.run = pb
            of_res.name = offense
            of_res.state_code = state
            of_res.county_name = county
            of_res.count = year_data
            of_res.save()

# method to get the climate stats
def get_climate_stats(count_state_list, pb):
    climate_stats = api_com.get_climate_information(count_state_list)

    for key, year_value in climate_stats.items():
        total_val = 0
        for i in range(2016, 2021):
            total_val += year_value[str(i)]

        county = key[0]
        state = key[1]
        precip = Precipitation()
        precip.run = pb
        precip.name = 'rainfall'
        precip.units = 'inches'
        precip.state_code = state
        precip.county_name = county
        precip.value = total_val * 2400
        precip.save()


# method to get the environmental data
def get_environmental_data(fips_ids, pb):
    fips_ids = [f.replace('FIPS_', '') for f in fips_ids]
    env_json = api_com.create_environmental_json(fips_ids)

    pollutants = set()
    fips_pols = {}
    for fips_key, data in env_json.items():
        fips_pols[fips_key] = []
        for pol, pol_data in data.items():
            fips_pols[fips_key].append(pol)
            pollutants.add((pol, pol_data['units']))

            precip = Pollutant()
            precip.run = pb
            precip.name = pol
            precip.units = pol_data['units']
            precip.fips_code = fips_key
            try:
                precip.value = float(pol_data['mean'])
            except TypeError:
                precip.value = float(pol_data['mean'][0])
            precip.save()

    # for fips_key, data in fips_pols.items():
    #     for pol, units in pollutants:
    #         if pol not in data:
    #             precip = Pollutant()
    #             precip.run = pb
    #             precip.name = pol
    #             precip.units = units
    #             precip.fips_code = fips_key
    #             precip.value = -1.0
    #             precip.save()


# method to return the county by id
def county_by_id(request, county_id):
    county = County.objects.get(pk=county_id)
    return render(request, 'county_details.html', {'county': county})
