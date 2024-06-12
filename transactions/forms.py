from django import forms
from .models import TransactionsModel

class TransactionsForm(forms.ModelForm):
    class Meta:
        model = TransactionsModel
        fields = ["amount", "transaction_type"]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account", None)
        super().__init__(*args, **kwargs)
        self.fields["transaction_type"].disabled = True
        self.fields["transaction_type"].widget = forms.HiddenInput()
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control w-100"})
            
            
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transactions = self.account.balance + self.cleaned_data.get("amount")
        return super().save(commit)
    
    
class DepositForm(TransactionsForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get("amount")
        if amount < min_deposit_amount:
            raise forms.ValidationError(f"You need at least {min_deposit_amount} $")
        return amount
