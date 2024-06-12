from django.urls import path
from .import views

urlpatterns = [
    path("deposit/", views.DepositMoneyView.as_view(), name="deposit_money")
]
