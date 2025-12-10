import re
import ijson
from django.core.management.base import BaseCommand
from cases.models import Case
from django.utils.dateparse import parse_date, parse_datetime
from django.contrib.auth.models import User

BATCH_SIZE = 1000  # For progress logging


def safe_parse_date(value):
    if isinstance(value, str) and value.strip():
        try:
            return parse_date(value)
        except Exception:
            return None
    return None


def safe_parse_datetime(value):
    if isinstance(value, str) and value.strip():
        try:
            return parse_datetime(value)
        except Exception:
            return None
    return None


def parse_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['yes', 'true', '1']
    return False


class Command(BaseCommand):
    help = "Stream-import Mombasa Case data from a large JSON file efficiently"

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='case_occurence.json', help='Path to JSON file')

    def handle(self, *args, **options):
        file_path = options['file']

        created, updated, skipped, user_created = 0, 0, 0, 0
        existing_users = {u.username: u for u in User.objects.all()}

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Use ijson to stream parse the JSON array
                parser = ijson.items(f, 'item')

                for i, entry in enumerate(parser, start=1):
                    try:
                        # Only import cases where county is "mombasa"
                        if entry.get("incident_report_county_code", "").strip().lower() != "mombasa":
                            continue

                        case_id = entry.get("case_id") or entry.get("id")
                        if not case_id:
                            skipped += 1
                            continue

                        # Handle assigned user
                        assigned_to = entry.get("assigned_to")
                        user_obj = None
                        if assigned_to:
                            username = assigned_to.strip().lower().replace(" ", "_")
                            if username in existing_users:
                                user_obj = existing_users[username]
                            else:
                                user_obj = User(username=username)
                                user_obj.set_password("12345")
                                user_obj.save()
                                existing_users[username] = user_obj
                                user_created += 1

                        # Prepare case defaults
                        case_defaults = {
                            "assigned_to": assigned_to,
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

                        # Update or create case
                        case_obj, is_created = Case.objects.update_or_create(
                            case_id=case_id,
                            defaults=case_defaults
                        )

                        if user_obj and hasattr(case_obj, "user"):
                            case_obj.user = user_obj
                            case_obj.save(update_fields=["user"])

                        if is_created:
                            created += 1
                        else:
                            updated += 1

                        if i % BATCH_SIZE == 0:
                            self.stdout.write(f"Processed {i} records...")

                    except Exception as e:
                        skipped += 1
                        self.stderr.write(f"❌ Skipping entry {i} due to error: {e}")

        except Exception as e:
            self.stderr.write(f"❌ Failed to read or stream JSON: {e}")
            return

        self.stdout.write(self.style.SUCCESS(f"✅ Created cases: {created}"))
        self.stdout.write(self.style.SUCCESS(f"✅ Updated cases: {updated}"))
        self.stdout.write(self.style.SUCCESS(f"👤 New users created: {user_created}"))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped entries: {skipped}"))
