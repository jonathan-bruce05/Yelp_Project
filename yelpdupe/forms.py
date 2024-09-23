# Python file to regulate the Google Places API, used to accept requests.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, label='Search for Restaurants')
    distance = forms.IntegerField(min_value=1, max_value=50000, label='Distance (meters)', initial = 5000)
    min_rating = forms.FloatField(min_value=0, max_value=5, label='Minimum Rating', initial=4.0)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = ('username', 'email', 'password1', 'password2')