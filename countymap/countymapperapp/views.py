from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
from .models import County

# base index page
def index(request):
    if request.method == 'POST':
        print(request.POST.get('state_field'))
        #if request.POST.get('submit_state_county_button'):
        statefield = request.POST.get('state_field')
        countyfield = request.POST.get('county_field')
        print(f'hi{countyfield}, {statefield}')

# base index page
def index(request):
    return redirect('homepage')

# homepage that the user will see on page arrival
def homepage(request):
    return render(request, 'homepage.html')

# method to return the county by id
def county_by_id(request, county_id):
    county = County.objects.get(pk=county_id)
    return render(request, 'county_details.html', {'county': county})
