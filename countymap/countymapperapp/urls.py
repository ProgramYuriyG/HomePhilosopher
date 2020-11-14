from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('county/<int:county_id>', views.county_by_id, name='county_by_id'),
]
