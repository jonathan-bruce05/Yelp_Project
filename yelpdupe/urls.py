from . import views
from django.urls import path
from .views import register, login_view, logout_view

app_name = "YelpDupe"

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]