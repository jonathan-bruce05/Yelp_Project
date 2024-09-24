from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from yelpdupe.forms import RegisterForm
from django.urls import reverse

# Define the index view
def index(request):
    return render(request, 'yelpdupe/index.html')  # Ensure you have an index.html template

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

    return render(request, 'yelpdupe/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to log in after logging out

