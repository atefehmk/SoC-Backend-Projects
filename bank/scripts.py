import random
from django.db import transaction
import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()
from account.models import Account
from person.models import Person

persons = [Person(first_name=f"First{i}", last_name=f"Last{i}", national_id=str(i).zfill(10)) for i in range(1000)]
Person.objects.bulk_create(persons)

persons = list(Person.objects.all())


batch_size = 100000
for i in range(0, 1000000, batch_size):
    accounts = [Account(owner=random.choice(persons), account_id=f"ACC{i+j}", balance=random.uniform(1000, 10000000)) for j in range(batch_size)]
    with transaction.atomic():
        Account.objects.bulk_create(accounts)
