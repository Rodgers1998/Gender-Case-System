from django.db import models
from django.contrib.auth.models import User
import uuid


class Case(models.Model):
    case_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    assigned_to = models.CharField(max_length=150, null=True, blank=True)
    previous_case_number = models.CharField(max_length=100, null=True, blank=True)

    case_number = models.CharField(max_length=100, null=True, blank=True)
    case_name = models.CharField(max_length=255, null=True, blank=True)
    case_summary_notes = models.TextField(null=True, blank=True)

    date_of_case_reporting = models.DateField(null=True, blank=True)
    date_of_case_intake = models.DateField(null=True, blank=True)
    date_of_case_assignment = models.DateField(null=True, blank=True)
    date_of_case_closure = models.DateField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    date_of_court_followup = models.DateField(null=True, blank=True)
    date_of_safe_house_onboarding = models.DateField(null=True, blank=True)
    date_of_safe_house_discharge = models.DateField(null=True, blank=True)

    case_reporting_datekey = models.IntegerField(null=True, blank=True)
    case_intake_datekey = models.IntegerField(null=True, blank=True)

    case_duration_in_days = models.IntegerField(null=True, blank=True)
    days_since_intake = models.IntegerField(null=True, blank=True)

    gender_site_code_of_reporting = models.CharField(max_length=10, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)

    assault_type = models.CharField(max_length=100, null=True, blank=True)
    cleaned_assault_type = models.CharField(max_length=100, null=True, blank=True)

    referred_to_safe_house = models.BooleanField(default=False)
    referred_to_other_shofco_programs = models.BooleanField(default=False)
    referred_to_dco = models.BooleanField(default=False)
    referred_to_counseling_and_support = models.BooleanField(default=False)
    referred_to_police = models.BooleanField(default=False)
    referred_for_medical_intervention = models.BooleanField(default=False)
    case_referred_to_location = models.TextField(null=True, blank=True)

    case_reported_to_police = models.BooleanField(null=True, blank=True)
    reported_by = models.CharField(max_length=100, null=True, blank=True)

    parent_case_id = models.UUIDField(null=True, blank=True)
    parent_case_type = models.CharField(max_length=100, null=True, blank=True)

    incident_report_village_name = models.CharField(max_length=100, null=True, blank=True)
    incident_report_ward_code = models.CharField(max_length=50, null=True, blank=True)
    incident_report_constituency_code = models.CharField(max_length=50, null=True, blank=True)
    incident_report_county_code = models.CharField(max_length=50, null=True, blank=True)

    case_is_closed = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    is_case_referred = models.BooleanField(default=False)
    is_the_case_proceeding_to_court = models.BooleanField(null=True, blank=True)
    case_still_in_court = models.BooleanField(null=True, blank=True)
    stage_of_case_in_court = models.CharField(max_length=100, null=True, blank=True)

    medium_of_reporting = models.CharField(max_length=100, null=True, blank=True)
    survivor_gender = models.CharField(max_length=20, null=True, blank=True)
    survivor_age = models.IntegerField(null=True, blank=True)
    age_group = models.CharField(max_length=50, null=True, blank=True)

    county = models.CharField(max_length=100, null=True, blank=True)
    case_constituency_name = models.CharField(max_length=100, null=True, blank=True)
    case_ward_name = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.case_number or self.case_id}"
