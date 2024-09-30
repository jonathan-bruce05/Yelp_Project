from . import views
from django.urls import path, include
from .views import (map_view, search_restaurants, home, register, login_view, logout_view
, reset_password, search_username, reviews_viewer, toggle_favorite)

# app_name = "YelpDupe"

urlpatterns = [
    path('search/', search_restaurants, name='search_restaurants'),
    path('map/', map_view, name='map'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('accounts/', include('allauth.urls')),

    path('reset_password/', views.search_username, name='search_username'),
    path('reset_password/<str:username>/', views.reset_password, name='reset_password'),

    path('restaurant/<str:place_id>/', views.restaurant_details, name='restaurant_details'),
    path('reviews/', reviews_viewer, name='reviews_viewer'),
    path('write_review/<str:place_id>/<str:restaurant_name>/', views.write_review, name='write_review'),
    path('restaurant/<str:place_id>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_restaurants, name='favorite_restaurants'),

]