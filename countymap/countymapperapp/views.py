from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup


from .models import County
from django.shortcuts import redirect

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
