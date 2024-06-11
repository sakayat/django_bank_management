from django.db import models
from accounts.models import UserBankAccount
from .constants import account_type
# Create your models here.
class TransactionsModel(models.Model):
    account = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transactions = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=account_type, null=True)
    timestamps = models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["timestamps"]
        
        
    def __str__(self):
        return str(self.account)
