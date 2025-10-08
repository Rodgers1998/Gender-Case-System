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
            # Case Identification
            'case_number', 'case_name', 'previous_case_number', 'assigned_to',

            # Dates
            'date_of_case_reporting', 'date_of_case_intake',
            'date_of_case_assignment', 'date_of_case_closure',
            'date_modified', 'date_of_court_followup',
            'date_of_safe_house_onboarding', 'date_of_safe_house_discharge',

            # Case Info
            'case_summary_notes', 'assault_type', 'cleaned_assault_type',
            'gender_site_code_of_reporting', 'site',
            'case_duration_in_days', 'days_since_intake',
            'medium_of_reporting', 'reported_by',

            # Referrals
            'referred_to_safe_house', 'referred_to_other_shofco_programs',
            'referred_to_dco', 'referred_to_counseling_and_support',
            'referred_to_police', 'referred_for_medical_intervention',
            'case_referred_to_location', 'case_reported_to_police',

            # Court
            'is_the_case_proceeding_to_court', 'case_still_in_court',
            'stage_of_case_in_court',

            # Survivor Info
            'survivor_gender', 'survivor_age', 'age_group',

            # Location Info
            'county', 'case_constituency_name', 'case_ward_name',
            'incident_report_village_name', 'incident_report_ward_code',
            'incident_report_constituency_code', 'incident_report_county_code',

            # Relationships
            'parent_case_id', 'parent_case_type',

            # Status
            'case_is_closed', 'is_case_referred', 'closed',
        ]

        widgets = {
            # Text Fields
            'case_number': forms.TextInput(attrs={'class': 'form-control'}),
            'case_name': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_case_number': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.TextInput(attrs={'class': 'form-control'}),
            'assault_type': forms.TextInput(attrs={'class': 'form-control'}),
            'cleaned_assault_type': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
            'gender_site_code_of_reporting': forms.TextInput(attrs={'class': 'form-control'}),
            'medium_of_reporting': forms.TextInput(attrs={'class': 'form-control'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            'case_summary_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'case_referred_to_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'stage_of_case_in_court': forms.TextInput(attrs={'class': 'form-control'}),
            'age_group': forms.TextInput(attrs={'class': 'form-control'}),

            # Numbers
            'survivor_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'case_duration_in_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'days_since_intake': forms.NumberInput(attrs={'class': 'form-control'}),

            # Selects
            'survivor_gender': forms.Select(
                choices=[('male', 'Male'), ('female', 'Female')],
                attrs={'class': 'form-control'}
            ),

            # Dates
            'date_of_case_reporting': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_case_intake': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_case_assignment': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_case_closure': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_modified': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_of_court_followup': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_safe_house_onboarding': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_safe_house_discharge': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            # Booleans (Checkboxes)
            'referred_to_safe_house': forms.CheckboxInput(),
            'referred_to_other_shofco_programs': forms.CheckboxInput(),
            'referred_to_dco': forms.CheckboxInput(),
            'referred_to_counseling_and_support': forms.CheckboxInput(),
            'referred_to_police': forms.CheckboxInput(),
            'referred_for_medical_intervention': forms.CheckboxInput(),
            'case_reported_to_police': forms.CheckboxInput(),
            'is_the_case_proceeding_to_court': forms.CheckboxInput(),
            'case_still_in_court': forms.CheckboxInput(),
            'case_is_closed': forms.CheckboxInput(),
            'is_case_referred': forms.CheckboxInput(),
            'closed': forms.CheckboxInput(),
        }
