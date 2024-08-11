# SoC-Backend-Projects

This repository contains backend projects for the SoC course. The `queries.py` file includes various queries related to account and person management. You can run specific queries using the command-line interface.

## Running Queries

To execute a query, run the following command:

```bash
python queries.py [query_name]
```

### Available Queries
1. **list_accounts:** List the name of each account owner and the balance of each account.
2. **max_balance_account:** Retrieve the account with the highest balance.
3. **min_balance_accounts:** Retrieve the top 5 accounts with the lowest balance.
4. **transfer_funds:** Transfer a specified amount of money from one account to another.
5. **accounts_id_gt_balance:** List accounts where the account ID is greater than the balance.
6. **accounts_nid_gt_balance:** List accounts where the owner's national ID is greater than the balance.
7. **index_benchmark:** Retrieve accounts with balances over 2 million or under 1 million from a pre-existing dataset of 10 million random records. This query assesses performance with and without an index on the `balance` column.
8. **sum_person_balances:** Calculate and list the total balance for each person in the bank.

## Outputs
The outputs of the queries are logged in separate files. After running a query, you can check the corresponding log file to view the results. The log files are named [query_name].log.
## Example
To get the account with the highest balance, use:
```bash
python queries.py max_balance_account
```
 The output will be stored in max_balance_account.log.
