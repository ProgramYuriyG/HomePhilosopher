from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.template import RequestContext

from .models import County

# base index page
def index(request):
    return redirect('homepage')

# homepage that the user will see on page arrival
def homepage(request):
    if request.method == 'POST':
        statefield = request.POST.get('state_field')
        countyfield = request.POST.get('county_field')
        print(f'-{countyfield}, {statefield}')
        context = {'state_field': statefield,
                   'county_field': countyfield}
        return render_to_response('homepage.html', context)
    return render(request, 'homepage.html')

# method to return the county by id
def county_by_id(request, county_id):
    county = County.objects.get(pk=county_id)
    return render(request, 'county_details.html', {'county': county})
