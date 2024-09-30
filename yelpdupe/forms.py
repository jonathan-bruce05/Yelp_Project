# Python file to regulate the Google Places API, used to accept requests.

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from yelpdupe.models import Review
User = get_user_model()


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=True)
    distance = forms.IntegerField(required=False, min_value=100, max_value=50000)  # Optional field
    min_rating = forms.FloatField(required=False, min_value=1, max_value=5)  # Optional field



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class UsernameForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 5}),
        }