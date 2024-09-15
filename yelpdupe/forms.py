# Python file to regulate the Google Places API, used to accept requests.

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, label='Search for Restaurants')