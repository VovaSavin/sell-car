from django import forms
from django.core.exceptions import ValidationError
from .models import CarAdvertisement, ImageCars, MyUser
import time
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class CarAdvertisementForm(forms.ModelForm):
    """Форма для создания обьявления о продаже авто на стороне пользователя"""

    brand = forms.CharField(
        label="Марка:",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Марка авто..."}
        )
    )
    model_car = forms.CharField(
        label="Модель:",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Модель авто..."}
        )
    )

    engine_volume = forms.CharField(
        label="Обьём двигателя:",
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Объём двигателя", "min": "0", "step": "0.1"}
        )
    )

    year = forms.CharField(
        label="Год выпуска:",
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Год выпуска...", "min": "1940", "max": time.strftime("%Y"), "step": "1"}
        )
    )
    odometr = forms.CharField(
        label="Пробег:",
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Пробег...", "min": "0", "step": "1"}
        )
    )

    color = forms.CharField(
        label="Цвет:",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Цвет..."}
        )
    )

    price = forms.CharField(
        label="Цена:",
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Цена...", "min": "0"}
        )
    )

    city = forms.CharField(
        label="Город:",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Город регистрации..."}
        )
    )

    header = forms.CharField(
        label="Заголовок:",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-sm-4 mb-2",
                   "placeholder": "Заголовок..."}
        )
    )

    description = forms.CharField(
        label="Описание:",
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "placeholder": "Описание...", "rows": 5}
        )
    )

    class Meta:
        model = CarAdvertisement
        fields = (
            "brand", "model_car", "typeauto", "fuel",
            "transmission", "engine_volume", "year", "odometr",
            "color", "price", "header", "city",
            "description",
        )


class ImageCarsForm(forms.ModelForm):
    """Форма загрузки изображений авто"""

    class Meta:
        model = ImageCars
        fields = (
            "image", "image2", "image3", "image4", "image5", "image6"
        )


class EditMyUser(forms.ModelForm):
    """Форма редактирования информации о пользователе"""

    phone = forms.CharField(
        label="Номер телефона:",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Phone number...", "maxlength": "12",
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
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.",
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Login..."
            }
        )
    )

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if data.isnumeric() == False:
            raise ValidationError("Номер должен содержать только цифры")
        return data

    class Meta:
        model = MyUser
        fields = (
            "username", "email", "city", "phone", "photo",
        )


class SendMail(forms.Form):
    """Форма саппорт"""

    problem = forms.CharField(
        label="Тема",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-sm-12 mb-2", "placeholder": "Проблема..."
            }
        )
    )
    text_problem = forms.CharField(
        label="Описание проблемы",
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "placeholder": "Детальное описание проблемы...", "rows": 5}
        )
    )

    captcha = ReCaptchaField()

    class Meta:
        fields = ["problem", "text_problem", "captcha", ]
