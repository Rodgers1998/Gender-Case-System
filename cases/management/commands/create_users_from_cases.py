import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = "Create users from assigned_to field in court_cases_only.json with default password '12345'"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'court_cases_only.json')

        if not os.path.exists(json_path):
            self.stderr.write(f"❌ File not found: {json_path}")
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)

        usernames = set()
        for case in cases:
            username = case.get('assigned_to')
            if username:
                usernames.add(username.strip().lower())

        created = 0
        for username in usernames:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    password='12345',
                    is_staff=False,
                    is_superuser=False
                )
                created += 1
                self.stdout.write(f"✅ Created user: {username}")
            else:
                self.stdout.write(f"ℹ️ User already exists: {username}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done. Created {created} new user(s)."))
