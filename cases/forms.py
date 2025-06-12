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
            'username': '',
            'first_name': '',
            'email': '',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don’t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'previous_case_number',
            'assigned_to',
            'date_of_case_reporting',
            'assault_type',
            'site',
            'cleaned_assault_type',
            'survivor_gender',
            'survivor_age',
            'age_group',
            'case_is_closed',
            'case_still_in_court',
            'stage_of_case_in_court',
        ]
        widgets = {
            'previous_case_number':forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_case_reporting': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'survivor_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.TextInput(attrs={'class': 'form-control'}),
            'assault_type': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
            'cleaned_assault_type': forms.TextInput(attrs={'class': 'form-control'}),
            'survivor_gender': forms.Select(choices=[('male', 'Male'), ('female', 'Female')], attrs={'class': 'form-control'}),
            'age_group': forms.TextInput(attrs={'class': 'form-control'}),
            'case_is_closed': forms.CheckboxInput(),
            'case_still_in_court': forms.CheckboxInput(),
            'stage_of_case_in_court': forms.TextInput(attrs={'class': 'form-control'}),
        }
