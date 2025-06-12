from django.contrib import admin
from .models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    # Display relevant fields based on the new model
    list_display = (
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
    )

    # Enable search on appropriate text fields
    search_fields = (
        'assigned_to',
        'assault_type',
        'cleaned_assault_type',
        'site',
        'stage_of_case_in_court',
    )

    # Useful filters
    list_filter = (
        'case_is_closed',
        'case_still_in_court',
        'survivor_gender',
        'age_group',
        'site',
    )

    ordering = ('-date_of_case_reporting',)
