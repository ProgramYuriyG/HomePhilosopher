from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage/', views.homepage, name='homepage'),
    path('county_mapper/', views.county_mapper, name='county_mapper'),
    path('county/<int:county_id>', views.county_by_id, name='county_by_id'),
]
