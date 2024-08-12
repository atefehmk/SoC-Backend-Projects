import random
from django.db import transaction, connection
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()
from account.models import Account
from person.models import Person

def reset_sqlite_sequence(model):
    with connection.cursor() as cursor:
        table_name = model._meta.db_table
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")

reset_sqlite_sequence(Person)
reset_sqlite_sequence(Account)

persons = [Person(first_name=f"First{i+1}", last_name=f"Last{i+1}", national_id=str(i+1).zfill(10)) for i in range(1000)]
Person.objects.bulk_create(persons)

persons = list(Person.objects.all())

batch_size = 1000
for i in range(0, 1000000, batch_size):
    accounts = [Account(owner=random.choice(persons), account_id=f"ACC{i+j+1}", balance=random.uniform(1, 10000000)) for j in range(batch_size)]
    with transaction.atomic():
        Account.objects.bulk_create(accounts)
