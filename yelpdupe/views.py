from django.shortcuts import render, redirect
from django.http import HttpResponse

#Imports used for Restaurant search
import requests
from yelpdupe.forms import SearchForm
from django.conf import settings

#
def home(request):
    return render(request, 'yelpdupe/home.html')

#Google Restaurant search implementation
def search_restaurants(request):
    form = SearchForm()  # Create an empty form instance
    results = []
    restaurant_locations = []  # This will store lat/lng/name for the map

    if request.method == 'POST':  # Check if the form was submitted
        form = SearchForm(request.POST)  # Bind data to the form
        if form.is_valid():  # Validate the form data
            query = form.cleaned_data['query']  # Get the cleaned data from the form
            distance = form.cleaned_data['distance'] or 5000  # Get the user-specified distance
            min_rating = form.cleaned_data['min_rating'] or 2 # Get the user-specified minimum rating

            location = '33.7490,-84.3880'  # Currently set to NY city

            url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
            params = {
                'query': query,  # Use the search query input by the user
                'type': 'restaurant',  # Specify the type of place to search
                'key': settings.GOOGLE_PLACES_KEY,  # Access the API key securely from settings
                'location': location,  # Center point of the search
                'radius': distance,  # Use the user-specified distance
            }
            response = requests.get(url, params=params)  # Make the API request
            if response.status_code == 200:  # Check if the request was successful
                all_results = response.json().get('results', [])  # Extract the results from the response

                # Filter results based on user-specified minimum rating
                results = [place for place in all_results if place.get('rating', 0) >= min_rating]

                # Optional: Sort results by rating descending
                results.sort(key=lambda x: x.get('rating', 0), reverse=True)
                for result in results:
                    if 'geometry' in result and 'location' in result['geometry']:
                        lat = result['geometry']['location']['lat']
                        lng = result['geometry']['location']['lng']
                        name = result.get('name', 'Unknown Restaurant')
                        restaurant_locations.append({
                            'name': name,
                            'lat': lat,
                            'lng': lng
                        })
            else:
                results = []  # Handle errors gracefully
    request.session['restaurant_locations'] = restaurant_locations

    context = {
        'form': form,  # Pass the form to the template
        'results': results,  # Pass the search results to the template
    }
    return render(request, 'yelpdupe/search.html', context)  # Render the template with context
    # return redirect('map')
def map_view(request):
    # Example restaurant locations (latitude and longitude)
    locations = request.session.get('restaurant_locations', [])
    context = {
        'locations': locations,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_PLACES_KEY  # Add API key to context
    }

    return render(request, 'yelpdupe/map.html', context)