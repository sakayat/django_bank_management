from django import forms
from .models import TransactionsModel

class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionsModel
        fields = ["amount", "transaction_type"]
        
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disable = True
        self.fields['transaction_type'].widget = forms.HiddenInput()
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control w-100"})
        
    
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
    
        
