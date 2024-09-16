# Python file to regulate the Google Places API, used to accept requests.

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, label='Search for Restaurants')
    distance = forms.IntegerField(min_value=1, max_value=50000, label='Distance (meters)', initial = 5000)
    min_rating = forms.FloatField(min_value=0, max_value=5, label='Minimum Rating', initial=4.0)