# Python file to regulate the Google Places API, used to accept requests.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from yelpdupe.models import Review


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=True)
    distance = forms.IntegerField(required=False, min_value=100, max_value=50000)  # Optional field
    min_rating = forms.FloatField(required=False, min_value=1, max_value=5)  # Optional field



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = ('username', 'email', 'password1', 'password2')


class UsernameForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 5}),
        }