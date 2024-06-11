from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = reverse_lazy("register")
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    