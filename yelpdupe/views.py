from datetime import datetime

from django.core.paginator import Paginator
import requests
from .models import Review
from django.shortcuts import render, redirect
from django.http import HttpResponse

#Imports used for Restaurant search

from yelpdupe.forms import SearchForm, ReviewForm
from django.conf import settings

#
def index(request):
    return HttpResponse("Hello. Yelp_Dupe")

# Getter for reviews based on place id
def get_reviews(place_id):
    url = url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={settings.GOOGLE_PLACES_KEY}"
    response = requests.get(url)

    # Error Handling
    if response.status_code != 200:
        return []

    data = response.json()
    return data.get('result', {}).get('reviews', [])

def reviews_viewer(request):
    place_id = request.GET.get('place_id')
    google_reviews = get_reviews(place_id) if place_id else []
    user_reviews = Review.objects.filter(place_id=place_id)
    # display time
    for review in google_reviews:
        timestamp = review.get('time')
        review_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else None


    # Review form
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.place_id = place_id
            new_review.time = datetime.now()
            new_review.save()
            return redirect(request.path_info + f'?place_id={place_id}') #reloads page
    else:
        form = ReviewForm()

    # combines reviews into 1 list
    all_reviews = list(google_reviews) + list(user_reviews)

    # Pageifies reviews
    paginator = Paginator(all_reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'yelpdupe/reviewsearch.html', {
        'page_obj': page_obj,
        'place_id': place_id,
        'form': form,
    })

    # Find commit to main, figure out user auth confirmation/usrname
    # Write review
    # Push to database


#Google Restaurant search implementation
def search_restaurants(request):
    form = SearchForm()  # Create an empty form instance
    results = []
    restaurant_locations = []  # This will store lat/lng/name for the map

    if request.method == 'POST':  # Check if the form was submitted
        form = SearchForm(request.POST)  # Bind data to the form
        if form.is_valid():  # Validate the form data
            query = form.cleaned_data['query']  # Get the cleaned data from the form
            distance = form.cleaned_data['distance']  # Get the user-specified distance
            min_rating = form.cleaned_data['min_rating']  # Get the user-specified minimum rating

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