from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself', 'rows': 4}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
        }

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            raise forms.ValidationError("Website must start with 'http://' or 'https://'")
        return website
