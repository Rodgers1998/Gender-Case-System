import json
import os
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from django.conf import settings
from datetime import datetime
from cases.models import Case


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


def parse_datetime(value):
    if not value:
        return None
    try:
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return make_aware(dt) if settings.USE_TZ else dt
    except (ValueError, TypeError):
        return None


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == 'yes'
    return False


class Command(BaseCommand):
    help = "Import cases from JSON"

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='court_cases_only.json', help='Path to the JSON file to import')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']
        full_path = os.path.join(settings.BASE_DIR, file_path)

        if not os.path.exists(full_path):
            self.stdout.write(self.style.ERROR(f"❌ File not found: {full_path}"))
            return

        with open(full_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f"❌ JSON decode error: {e}"))
                return

        created_count = 0
        for entry in data:
            try:
                Case.objects.create(
                    case_id=entry.get("case_id"),
                    assigned_to=entry.get("assigned_to"),
                    previous_case_number=entry.get("previous_case_number"),
                    date_of_case_reporting=parse_date(entry.get("date_of_case_reporting")),
                    date_of_case_intake=parse_date(entry.get("date_of_case_intake")),
                    date_of_case_assignment=parse_date(entry.get("date_of_case_assignment")),
                    date_of_case_closure=parse_date(entry.get("date_of_case_closure")),
                    date_modified=parse_datetime(entry.get("date_modified")),
                    case_duration_in_days=entry.get("case_duration_in_days") or None,
                    days_since_intake=entry.get("days_since_intake") or None,
                    gender_site_code_of_reporting=entry.get("gender_site_code_of_reporting"),
                    site=entry.get("site"),
                    assault_type=entry.get("assault_type"),
                    cleaned_assault_type=entry.get("cleaned_assault_type"),
                    referred_to_safe_house=parse_bool(entry.get("referred_to_safe_house")),
                    referred_to_other_shofco_programs=parse_bool(entry.get("referred_to_other_shofco_programs")),
                    referred_to_dco=parse_bool(entry.get("referred_to_dco")),
                    referred_to_counseling_and_support=parse_bool(entry.get("referred_to_counseling_and_support")),
                    referred_to_police=parse_bool(entry.get("referred_to_police")),
                    referred_for_medical_intervention=parse_bool(entry.get("referred_for_medical_intervention")),
                    case_referred_to_location=entry.get("case_referred_to_location"),
                    incident_report_village_name=entry.get("incident_report_village_name"),
                    incident_report_ward_code=entry.get("incident_report_ward_code"),
                    incident_report_constituency_code=entry.get("incident_report_constituency_code"),
                    incident_report_county_code=entry.get("incident_report_county_code"),
                    case_is_closed=parse_bool(entry.get("case_is_closed")),
                    is_case_referred=parse_bool(entry.get("is_case_referred")),
                    is_the_case_proceeding_to_court=parse_bool(entry.get("is_the_case_proceeding_to_court")),
                    case_still_in_court=parse_bool(entry.get("case_still_in_court")),
                    date_of_court_followup=parse_date(entry.get("date_of_court_followup")),
                    stage_of_case_in_court=entry.get("stage_of_case_in_court"),
                    medium_of_reporting=entry.get("medium_of_reporting"),
                    survivor_gender=entry.get("survivor_gender"),
                    survivor_age=entry.get("survivor_age") or None,
                    age_group=entry.get("age_group"),
                    county=entry.get("county"),
                    case_constituency_name=entry.get("case_constituency_name"),
                    case_ward_name=entry.get("case_ward_name"),
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Skipping entry due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {created_count} cases."))
