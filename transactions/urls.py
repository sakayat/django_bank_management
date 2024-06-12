from django.urls import path
from .import views

urlpatterns = [
    path("deposit/", views.DepositMoneyView.as_view(), name="deposit_money"),
    path("withdraw/", views.WithdrawMoneyView.as_view(), name="withdraw_money")
]
