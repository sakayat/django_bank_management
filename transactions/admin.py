from typing import Any
from django.contrib import admin
from .models import TransactionsModel

# Register your models here.
@admin.register(TransactionsModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["account", "amount", "balance_after_transactions", "transaction_type", "loan_approve"]
    
    def save_model(self, request, obj, form, change):
        
        if obj.loan_approve == True:
            obj.account.balance += obj.amount
            obj.balance_after_transactions = obj.account.balance
            obj.account.save()
        return super().save_model(request, obj, form, change)