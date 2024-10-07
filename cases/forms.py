from django import forms
from .models import Case
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password', 'password2')
        help_texts = {
            'username': '',  # Remove help text for username
            'first_name': '',  # Remove help text for first_name
            'email': '',  # Remove help text for email
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don’t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Set the user's password
        if commit:
            user.save()
        return user


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'case_number', 
            'court_file_number',  # Added court file number
            'case_type', 
            'accused_name', 
            'accuser_name', 
            'accuser_phone', 
            'court_name',  
            'court_date', 
            'next_court_date', 
            'police_station',  
            'investigating_officer', 
            'investigating_officer_phone', 
            'stage_of_case',  
            'sub_county',  # Added sub-county
            'location', 
            'ward',  
        ]
        widgets = {
            'case_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Case Number'}),
            'court_file_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Court File Number'}),  # New widget for court file number
            'case_type': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for case types
            'accused_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accused Name'}),
            'accuser_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accuser Name'}),
            'accuser_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accuser Phone'}),
            'court_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Court Name'}),  
            'court_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_court_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'police_station': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Police Station'}),
            'investigating_officer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Officer Name'}),
            'investigating_officer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Officer Phone'}),
            'stage_of_case': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for stage of case
            'sub_county': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sub-County'}),  # New widget for sub-county
            'location': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for locations
            'ward': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Ward'}),  
        }
