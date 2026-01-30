import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role='admin')
    print("Superuser 'admin' created.")
else:
    print("Superuser 'admin' already exists.")

if not User.objects.filter(username='manager1').exists():
    User.objects.create_user('manager1', 'manager1@example.com', 'managerpass', role='manager')
    print("Manager 'manager1' created.")

if not User.objects.filter(username='emp1').exists():
    User.objects.create_user('emp1', 'emp1@example.com', 'emppass', role='employee')
    print("Employee 'emp1' created.")
