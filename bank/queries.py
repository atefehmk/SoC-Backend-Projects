import logging
import os
import sys
import django
import random
import time
from django.db import models, transaction, connection
from django.db.models import Sum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

from account.models import Account
from person.models import Person

def list_accounts():
    logging.basicConfig(filename='logs/list_accounts.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    accounts = Account.objects.all().select_related('owner')

    for account in accounts:
        logger.info(f"Owner: {account.owner.first_name} {account.owner.last_name}, Balance: {account.balance}")

def max_balance_account():
    logging.basicConfig(filename='logs/max_balance_account.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    max_balance_account = Account.objects.order_by('-balance').first()

    if max_balance_account:
        logger.info(f"Account with Max Balance: Owner: {max_balance_account.owner.first_name} {max_balance_account.owner.last_name}, Balance: {max_balance_account.balance}")
    else:
        logger.info("No accounts found.")

def min_balance_accounts():
    logging.basicConfig(filename='logs/min_balance_accounts.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    min_balance_accounts = Account.objects.order_by('balance')[:5]

    for account in min_balance_accounts:
        logger.info(f"Account: Owner: {account.owner.first_name} {account.owner.last_name}, Balance: {account.balance}")

def transfer_funds(from_account_id, to_account_id, amount):
    logging.basicConfig(filename='logs/transfer_funds.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        from_account = Account.objects.get(id=from_account_id)
        to_account = Account.objects.get(id=to_account_id)
        from_account.balance = float(from_account.balance)
        to_account.balance = float(to_account.balance)
    except Account.DoesNotExist:
        logger.error(f"Transfer failed: One or both accounts do not exist. From Account ID: {from_account_id}, To Account ID: {to_account_id}")
        return False

    if from_account.balance >= amount:
        logger.info(f"Before Transfer: from Account ID {from_account_id} to Account ID {to_account_id}. Old balances - From Account: {from_account.balance}, To Account: {to_account.balance}")
        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()

        logger.info(f"Transfer successful: {amount} transferred from Account ID {from_account_id} to Account ID {to_account_id}. New balances - From Account: {from_account.balance}, To Account: {to_account.balance}")
        return True
    else:
        logger.warning(f"Transfer failed: Insufficient funds in Account ID {from_account_id}. Attempted transfer amount: {amount}, Available balance: {from_account.balance}")
        return False

def accounts_id_gt_balance():
    logging.basicConfig(filename='logs/accounts_id_gt_balance.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    accounts = Account.objects.filter(id__gt=models.F('balance'))

    for account in accounts:
        logger.info(f"Account ID: {account.id}, Balance: {account.balance}")

def accounts_nid_gt_balance():
    logging.basicConfig(filename='logs/accounts_nid_gt_balance.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    accounts = Account.objects.filter(owner__national_id__gt=models.F('balance'))
    
    for account in accounts:
        logger.info(f"Account ID: {account.account_id}, Owner National ID: {account.owner.national_id}, Balance: {account.balance}")

def sum_person_balances():
    logging.basicConfig(filename='logs/sum_person_balances.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    person_balances = Person.objects.annotate(total_balance=Sum('accounts__balance'))
    
    for person in person_balances:
        logger.info(f"Name: {person.first_name} {person.last_name}, Total Balance: {person.total_balance}")

def index_benchmark():
    logging.basicConfig(filename='logs/index_benchmark.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    start_time = time.time()
    accounts_without_index = Account.objects.filter(balance__gt=2000000) | Account.objects.filter(balance__lt=1000000)
    logger.info(f"Execution time without index: {time.time() - start_time} seconds")

    with connection.cursor() as cursor:
        cursor.execute('DROP INDEX IF EXISTS balance_index')
        cursor.execute('CREATE INDEX balance_index ON account_account (balance)')

    start_time = time.time()
    accounts_with_index = Account.objects.filter(balance__gt=2000000) | Account.objects.filter(balance__lt=1000000)
    logger.info(f"Execution time with index: {time.time() - start_time} seconds")
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "list_accounts":
            list_accounts()
        elif sys.argv[1] == "max_balance_account":
            max_balance_account()
        elif sys.argv[1] == "min_balance_accounts":
            min_balance_accounts()
        elif sys.argv[1] == "transfer_funds":
            if len(sys.argv) == 5:
                from_account_id = sys.argv[2]
                to_account_id = sys.argv[3]
                amount = float(sys.argv[4])
                transfer_funds(from_account_id, to_account_id, amount)
        elif sys.argv[1] == "accounts_id_gt_balance":
            accounts_id_gt_balance()
        elif sys.argv[1] == "accounts_nid_gt_balance":
            accounts_nid_gt_balance()
        elif sys.argv[1] == "sum_person_balances":
            sum_person_balances()
        elif sys.argv[1] == "index_benchmark":
            index_benchmark()
        else:
            print("Invalid query")
    else:
        print("No query specified")
