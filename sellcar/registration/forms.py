from django import forms
from django.contrib.auth.forms import UserCreationForm
from advertisement.models import MyUser
from django.core.exceptions import ValidationError


class RegistrationCustomForm(UserCreationForm):
    """Fields for registration user on the client side"""
    phone = forms.CharField(
        label="Номер телефона (380xxxxxxxxx):",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Number(380 - не вводить!!!)...", "maxlength": "9",
            }
        )
    )
    city = forms.CharField(
        label="Город:",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Your city..."
            }
        )
    )
    photo = forms.ImageField(
        label="Фотография пользователя:",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "onchange": "previewFile()",
            }
        )
    )
    email = forms.EmailField(
        label="Електронная почта:",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Email..."
            }
        )
    )
    username = forms.CharField(
        label="Введите имя пользователя:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Login..."
            }
        )
    )
    password1 = forms.CharField(
        label="Введите пароль:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Password..."
            }
        )
    )
    password2 = forms.CharField(
        label="Повторите пароль:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Repeat password..."
            }
        )
    )

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if data.isnumeric() == False:
            raise ValidationError("Номер должен содержать только цифры")
        data = f"380{data}"
        return data

    class Meta:
        model = MyUser
        fields = [
            'username', 'email', 'city', 'phone', 'password1', 'password2', 'photo'
        ]
