from . import views
from django.urls import path, include
from .views import map_view, search_restaurants, home, register, login_view, logout_view

# app_name = "YelpDupe"

urlpatterns = [
    path('search/', search_restaurants, name='search_restaurants'),
    path('map/', map_view, name='map'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('accounts/', include('allauth.urls')),

    path('restaurant/<str:place_id>/', views.restaurant_details, name='restaurant_details'),
]