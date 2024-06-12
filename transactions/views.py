from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import TransactionsModel
from .forms import DepositForm, WithdrawForm, LoanRequestForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse

# Create your views here.
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    model = TransactionsModel
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"account": self.request.user.account})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepositMoneyView(TransactionCreateMixin):
    template_name = "transactions/deposit_form.html"
    form_class = DepositForm

    def get_initial(self):
        initial = {"transaction_type": 1}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=["balance"])
        
        messages.success(self.request, f"{amount}$ is deposited to your account successfully")
        return super().form_valid(form)
    

class WithdrawMoneyView(TransactionCreateMixin):
    template_name = "transactions/withdraw_form.html"
    form_class = WithdrawForm

    def get_initial(self):
        initial = {"transaction_type": 2}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        account = self.request.user.account
        account.balance -= amount
        account.save(update_fields=["balance"])
        
        messages.success(self.request, f"{amount}$ withdrawn successfully")
        return super().form_valid(form)

class LoanRequestView(TransactionCreateMixin):
    template_name = "transactions/loan_request_form.html"
    form_class = LoanRequestForm

    def get_initial(self):
        initial = {"transaction_type": 3}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        current_loan_count = TransactionsModel.objects.filter(account = self.request.user.account, transaction_type = 3, loan_approve = True).count()
        if current_loan_count >= 3:
            return HttpResponse("You Have crossed you loan limits")
        messages.success(self.request, f"Loan Request for {amount}$ successfully")
        return super().form_valid(form)