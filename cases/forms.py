from django import forms
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'case_type', 'accused_name', 'accuser_name', 'accuser_phone', 'court_date', 'next_court_date', 'investigating_officer', 'investigating_officer_phone', 'location']
        widgets = {
            'case_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Case Number'}),
            'case_type': forms.Select(attrs={'class': 'form-control'}),  # Use Select for dropdown
            'accused_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accused Name'}),
            'accuser_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accuser Name'}),
            'accuser_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Accuser Phone'}),
            'court_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_court_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'investigating_officer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Officer Name'}),
            'investigating_officer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Officer Phone'}),
            'location': forms.Select(attrs={'class': 'form-control'}),  # Use Select for dropdown
        }
