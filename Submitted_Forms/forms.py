from django import forms
from .models import SubmittedForm

class SubmittedFormForm(forms.ModelForm):
    class Meta:
        model = SubmittedForm
        fields = ['form_title', 'file']
        widgets = {
            'form_title': forms.TextInput(attrs={'placeholder': 'Enter form title'}),
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }
