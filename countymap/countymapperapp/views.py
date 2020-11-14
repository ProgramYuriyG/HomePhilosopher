from django.shortcuts import render
from django.http import HttpResponse

from .models import County

# base index page
def index(request):
    return HttpResponse('Homepage Goes Here')

# method to return the county by id
def county_by_id(request, county_id):
    county = County.objects.get(pk=county_id)
    return render(request, 'county_details.html', {'county': county})
