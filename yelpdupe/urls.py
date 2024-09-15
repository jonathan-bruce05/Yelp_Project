from . import views
from django.urls import path

#Restaurant search imports
from .views import search_restaurants

app_name = "YelpDupe"

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', search_restaurants, name='search_restaurants'),
]