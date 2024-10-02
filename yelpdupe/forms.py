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



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    # Optionally, override this method if you need custom validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose another one.")
        return email

class UsernameForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us your thoughts'}),
        }