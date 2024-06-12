from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import TransactionsModel
from .forms import DepositForm
from django.contrib import messages
from django.urls import reverse_lazy


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
        return super().form_valid(form)
