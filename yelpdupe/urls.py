from . import views
from django.urls import path
from .views import map_view, search_restaurants
from .views import reviews_viewer

# app_name = "YelpDupe"

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', search_restaurants, name='search_restaurants'),
    path('map/', map_view, name='map'),
    path('reviews/', reviews_viewer, name='reviews_viewer'),
]