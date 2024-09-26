from . import views
from django.urls import path
from .views import map_view, search_restaurants, home

# app_name = "YelpDupe"

urlpatterns = [
    path('search/', views.search_restaurants, name='search_restaurants'),
    path('map/', views.map_view, name='map'),
    path('', views.home, name='home'),
    path('signin/', views.log_in, name='signIn'),
    path('restaurant/<str:place_id>/', views.restaurant_details, name='restaurant_details'),
]