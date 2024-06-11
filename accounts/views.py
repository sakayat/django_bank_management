from django.contrib.auth import login, logout
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = reverse_lazy("login")
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = "accounts/user_login.html"
    def get_success_url(self) -> str:
        return reverse_lazy("home")
    

class UserLogoutView(LogoutView):
    def get_success_url(self) -> str:
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy("home")
    