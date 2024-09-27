from datetime import datetime

from django.core.paginator import Paginator
import requests
from .models import Review
from django.shortcuts import render, redirect
from django.http import HttpResponse

#Imports used for Restaurant search
from yelpdupe.forms import SearchForm, ReviewForm
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from yelpdupe.forms import RegisterForm
from django.urls import reverse

#Password reset
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsernameForm
#
def home(request):
    return render(request, 'yelpdupe/home.html')

# Define the index view
def index(request):
    return render(request, 'yelpdupe/index.html')  # Ensure you have an index.html template

#Google Restaurant search implementation
def search_restaurants(request):
    form = SearchForm()  # Create an empty form instance
    results = []
    restaurant_locations = []  # This will store lat/lng/name for the map
    # Set a default location (e.g., Atlanta's coordinates)
    location = '33.7490,-84.3880'  # Atlanta, GA coordinates as default center

    if request.method == 'POST':  # Check if the form was submitted
        form = SearchForm(request.POST)  # Bind data to the form
        if form.is_valid():  # Validate the form data
            query = form.cleaned_data['query']  # Get the cleaned data from the form
            distance = form.cleaned_data['distance'] or 5000  # Get the user-specified distance
            min_rating = form.cleaned_data['min_rating'] or 2 # Get the user-specified minimum rating

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
                        place_id = result.get('place_id', None)  # Get the place_id for linking

                        # Only add the restaurant if a place_id is available
                        if place_id:
                            restaurant_locations.append({
                                'name': name,
                                'lat': lat,
                                'lng': lng,
                                'place_id': place_id,  # Make sure place_id is included
                                'address': result.get('formatted_address', 'No address available'),
                                'rating': result.get('rating', 'No rating available'),
                                'reviews': result.get('user_ratings_total', 'No reviews available')
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



def restaurant_details(request, place_id):
    # Get restaurant details from the session (or database if needed)
    restaurant = None
    restaurant_locations = request.session.get('restaurant_locations', [])

    # Find restaurant by place_id in the session
    for location in restaurant_locations:
        if location['place_id'] == place_id:
            restaurant = location
            break

    if not restaurant:
        return HttpResponse("Restaurant not found", status=404)

    # Pass the restaurant's lat/lng and other details to the template
    context = {
        'restaurant': restaurant,
        'lat': restaurant['lat'],  # Pass the latitude
        'lng': restaurant['lng'],  # Pass the longitude
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_PLACES_KEY
    }
    return render(request, 'yelpdupe/restaurant_detail.html', context)



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



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend to be used for authentication
            backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=backend)  # Log the user in with the correct backend
            return redirect(reverse('yelpdupe:index'))  # Redirect to a home page after successful registration
    else:
        form = RegisterForm()

    return render(request, 'yelpdupe/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('yelpdupe:index'))  # Using the namespace here
    else:
        form = AuthenticationForm()

    return render(request, 'yelpdupe/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to log in after logging out


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend to be used for authentication
            backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=backend)  # Log the user in with the correct backend
            return redirect('home')  # Redirect to a home page after successful registration
    else:
        form = RegisterForm()

    return render(request, 'yelpdupe/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('yelpdupe:index'))  # Using the namespace here
    else:
        form = AuthenticationForm()

    return render(request, 'yelpdupe/signIn.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to log in after logging out

# Step 2a: View for searching username and handling password reset
def search_username(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                # Redirect to the reset password form
                return redirect('reset_password', username=username)
            except User.DoesNotExist:
                messages.error(request, 'Username not found.')
    else:
        form = UsernameForm()

    return render(request, 'yelpdupe/search_username.html', {'form': form})

# Step 2b: Password reset view
def reset_password(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Invalid username.')
        return redirect('search_username')

    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'yelpdupe/reset_password.html', {'username': username})
