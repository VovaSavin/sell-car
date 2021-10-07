from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.RegistrateView.as_view(), name="registration")
]
