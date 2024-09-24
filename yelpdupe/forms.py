# Python file to regulate the Google Places API, used to accept requests.

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=True)
    distance = forms.IntegerField(required=False, min_value=100, max_value=50000)  # Optional field
    min_rating = forms.IntegerField(required=False, min_value=1, max_value=5)  # Optional field