from . import views
from django.urls import path
from .views import map_view, search_restaurants, home, signup

# app_name = "YelpDupe"

urlpatterns = [
    path('search/', search_restaurants, name='search_restaurants'),
    path('map/', map_view, name='map'),
    path('', home, name='home'),
    path('signup/', signup, name='signup')
]