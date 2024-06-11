from typing import Any
from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .constants import gender_type, account_type
from .models import UserBankAccount, UserAddress


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    account_type = forms.ChoiceField(choices=account_type)
    gender = forms.ChoiceField(choices=gender_type)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "birth_date",
            "account_type",
            "gender",
            "street_address",
            "city",
            "postal_code",
            "country"
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            birth_date = self.cleaned_data.get("birth_date")
            account_type = self.cleaned_data.get("account_type")
            gender = self.cleaned_data.get("gender")
            postal_code = self.cleaned_data.get("postal_code")
            country = self.cleaned_data.get("country")
            city = self.cleaned_data.get("city")
            street_address = self.cleaned_data.get("street_address")

            UserAddress.objects.create(
                user=user,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )

            UserBankAccount.objects.create(
                user=user,
                account_number=143590+user.id,
                account_type=account_type,
                birth_date=birth_date,
                gender=gender,
            )

            return user

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control w-100"})
