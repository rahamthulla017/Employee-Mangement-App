import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tasks.models import Project

count = Project.objects.count()
print(f"Total Projects: {count}")

if count == 0:
    print("Creating a sample project...")
    Project.objects.create(
        name="Internal Operations",
        description="General internal tasks",
        start_date="2026-01-01",
        end_date="2026-12-31",
        status="active"
    )
    print("Sample project created.")
else:
    print("Projects exist.")
    for p in Project.objects.all():
        print(f"- {p.name}")
