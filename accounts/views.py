from django.urls import reverse_lazy
from django.views import generic

from accounts.forms.sign_up_form import CustomUserCreationForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
