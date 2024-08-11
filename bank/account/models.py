from django.db import models

# Create your models here.
class Account(models.Model):
    owner = models.ForeignKey(to='person.Person', on_delete=models.CASCADE, related_name='accounts')
    account_id = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2)