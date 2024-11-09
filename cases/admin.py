from django.contrib import admin
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    # Display all fields in the list view
    list_display = (
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
        'sentence_duration', 
        'jail_duration',
        'county', 
        'sub_county', 
        'location', 
        'ward'
    )

    # Add search fields to easily locate cases by specific fields
    search_fields = (
        'case_number', 
        'court_file_number', 
        'accused_name', 
        'accuser_name', 
        'investigating_officer'
    )

    # Add filters for specific fields to refine displayed results
    list_filter = (
        'case_type', 
        'county', 
        'sub_county', 
        'stage_of_case', 
        'court_date'
    )

    # Define default ordering
    ordering = ('court_date', 'case_number')
