# SoC-Backend-Projects

This repository contains backend projects for the SoC course. The `queries.py` file includes various queries related to account and person management. You can run specific queries using the command-line interface.

## Running Queries

To execute a query, run the following command:

```bash
python queries.py [query_name]
```

Available Queries
list_accounts: List the name of each account owner and the balance of each account.
max_balance_account: Retrieve the account with the highest balance.
min_balance_accounts: Retrieve the top 5 accounts with the lowest balance.
transfer_funds: Transfer a specified amount of money from one account to another.
accounts_id_gt_balance: List accounts where the account ID is greater than the balance.
accounts_nid_gt_balance: List accounts where the owner's national ID is greater than the balance.
sum_person_balances: Calculate and list the total balance for each person in the bank.


