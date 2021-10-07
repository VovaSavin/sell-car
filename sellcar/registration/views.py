from django.contrib.auth.models import User
from .forms import RegistrationCustomForm
from django.views.generic import CreateView


# Create your views here.


class RegistrateView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = RegistrationCustomForm
    success_url = '/'
    template_name = 'registration/registration.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrateView, self).get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context
