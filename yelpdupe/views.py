from django.shortcuts import render
from django.http import HttpResponse

#Imports used for Restaurant search
import requests
from yelpdupe.forms import SearchForm
from django.conf import settings


def index(request):
    return HttpResponse("Hello. Yelp_Dupe")


#Google Restaurant search implementation
def search_restaurants(request):
    form = SearchForm()  # Create an empty form instance
    results = []
    if request.method == 'POST':  # Check if the form was submitted
        form = SearchForm(request.POST)  # Bind data to the form
        if form.is_valid():  # Validate the form data
            query = form.cleaned_data['query']  # Get the cleaned data from the form
            url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
            params = {
                'query': query,  # Use the search query input by the user
                'type': 'restaurant',  # Specify the type of place to search
                'key': settings.GOOGLE_PLACES_KEY,  # Access the API key securely from settings
            }
            response = requests.get(url, params=params)  # Make the API request
            if response.status_code == 200:  # Check if the request was successful
                results = response.json().get('results', [])  # Extract the results from the response
            else:
                results = []  # Handle errors gracefully

    context = {
        'form': form,  # Pass the form to the template
        'results': results,  # Pass the search results to the template
    }
    return render(request, 'yelpdupe/search.html', context)  # Render the template with context
