import json
from django.core.management.base import BaseCommand
from cases.models import Case
from django.utils.dateparse import parse_date, parse_datetime
from django.contrib.auth.models import User

def safe_parse_date(value):
    return parse_date(value) if isinstance(value, str) and value.strip() else None

def safe_parse_datetime(value):
    return parse_datetime(value) if isinstance(value, str) and value.strip() else None

def parse_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['yes', 'true', '1']
    return False

class Command(BaseCommand):
    help = "Import or update Case data from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='case_occurence.json', help='Path to the JSON file')

    def handle(self, *args, **options):
        file_path = options['file']
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(f"❌ Failed to read JSON: {e}")
            return

        created, updated, skipped = 0, 0, 0

        for entry in data:
            try:
                case_id = entry.get("case_id") or entry.get("id")
                if not case_id:
                    skipped += 1
                    continue

                case_obj, is_created = Case.objects.update_or_create(
                    case_id=case_id,
                    defaults={
                        "assigned_to": entry.get("assigned_to"),
                        "previous_case_number": entry.get("previous_case_number"),
                        "date_of_case_reporting": safe_parse_date(entry.get("date_of_case_reporting")),
                        "date_of_case_intake": safe_parse_date(entry.get("date_of_case_intake")),
                        "date_of_case_assignment": safe_parse_date(entry.get("date_of_case_assignment")),
                        "date_of_case_closure": safe_parse_date(entry.get("date_of_case_closure")),
                        "date_modified": safe_parse_datetime(entry.get("date_modified")),
                        "case_duration_in_days": entry.get("case_duration_in_days") or None,
                        "days_since_intake": entry.get("days_since_intake") or None,
                        "gender_site_code_of_reporting": entry.get("gender_site_code_of_reporting"),
                        "site": entry.get("site"),
                        "assault_type": entry.get("assault_type"),
                        "cleaned_assault_type": entry.get("cleaned_assault_type"),
                        "referred_to_safe_house": parse_boolean(entry.get("referred_to_safe_house")),
                        "referred_to_other_shofco_programs": parse_boolean(entry.get("referred_to_other_shofco_programs")),
                        "referred_to_dco": parse_boolean(entry.get("referred_to_dco")),
                        "referred_to_counseling_and_support": parse_boolean(entry.get("referred_to_counseling_and_support")),
                        "referred_to_police": parse_boolean(entry.get("referred_to_police")),
                        "referred_for_medical_intervention": parse_boolean(entry.get("referred_for_medical_intervention")),
                        "case_referred_to_location": entry.get("case_referred_to_location"),
                        "incident_report_village_name": entry.get("incident_report_village_name"),
                        "incident_report_ward_code": entry.get("incident_report_ward_code"),
                        "incident_report_constituency_code": entry.get("incident_report_constituency_code"),
                        "incident_report_county_code": entry.get("incident_report_county_code"),
                        "case_is_closed": parse_boolean(entry.get("case_is_closed")),
                        "is_case_referred": parse_boolean(entry.get("is_case_referred")),
                        "is_the_case_proceeding_to_court": parse_boolean(entry.get("is_the_case_proceeding_to_court")),
                        "case_still_in_court": parse_boolean(entry.get("case_still_in_court")),
                        "date_of_court_followup": safe_parse_date(entry.get("date_of_court_followup")),
                        "stage_of_case_in_court": entry.get("stage_of_case_in_court"),
                        "medium_of_reporting": entry.get("medium_of_reporting"),
                        "survivor_gender": entry.get("survivor_gender"),
                        "survivor_age": entry.get("survivor_age") or None,
                        "age_group": entry.get("age_group"),
                        "county": entry.get("county"),
                        "case_constituency_name": entry.get("case_constituency_name"),
                        "case_ward_name": entry.get("case_ward_name"),
                    }
                )

                # Auto-link user if present
                if entry.get("assigned_to"):
                    username = entry["assigned_to"].strip().lower().replace(" ", "_")
                    user, _ = User.objects.get_or_create(username=username, defaults={"password": "12345"})
                    case_obj.user = user
                    case_obj.save()

                if is_created:
                    created += 1
                else:
                    updated += 1
            except Exception as e:
                skipped += 1
                self.stderr.write(f"❌ Skipping entry due to error: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ Created: {created}"))
        self.stdout.write(self.style.SUCCESS(f"✅ Updated: {updated}"))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped: {skipped}"))
