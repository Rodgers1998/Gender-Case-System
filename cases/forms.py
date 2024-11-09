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
            'court_file_number',  
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
            'county',
            'sub_county',
            'location', 
            'ward',
            'sentence_duration',  # Added field for sentencing duration
            'jail_duration',      # Added field for jailing duration
        ]
        widgets = {
            'case_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Case Number'}),
            'court_file_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Court File Number'}),
            'case_type': forms.Select(attrs={'class': 'form-control'}),
            'accused_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accused Name'}),
            'accuser_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accuser Name'}),
            'accuser_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accuser Phone'}),
            'court_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Court Name'}),  
            'court_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_court_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'police_station': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Police Station'}),
            'investigating_officer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Officer Name'}),
            'investigating_officer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Officer Phone'}),
            'stage_of_case': forms.Select(attrs={'class': 'form-control'}), 
            'county': forms.Select(attrs={'class': 'form-control'}),
            'sub_county': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'ward': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Ward'}),
            'sentence_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sentencing duration (e.g., "2 years")'}),
            'jail_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter jailing duration (e.g., "2 years")'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        stage_of_case = cleaned_data.get('stage_of_case')
        sentence_duration = cleaned_data.get('sentence_duration')
        jail_duration = cleaned_data.get('jail_duration')

        # Validation for sentencing duration
        if stage_of_case == 'sentencing' and not sentence_duration:
            self.add_error('sentence_duration', "Please specify the sentencing duration.")
        
        # Validation for jailing duration
        if stage_of_case == 'jailing' and not jail_duration:
            self.add_error('jail_duration', "Please specify the jailing duration.")
        
        return cleaned_data
