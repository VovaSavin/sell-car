from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from PIL import Image


# Create your models here.


class Category(models.Model):
    """Модель для типа кузова авто"""
    body = models.CharField(max_length=100, verbose_name="Тип кузова")

    def __str__(self) -> str:
        return f"{self.body}"

    class Meta:
        verbose_name = 'Кузов'
        verbose_name_plural = 'Кузова'


def img_directory_path(instance, filename):
    return f"{instance.username}-{filename}"


class MyUser(AbstractUser):
    """Переопределённая модель пользователя"""
    phone = models.CharField(verbose_name="Номер телефона", max_length=14)
    city = models.CharField(verbose_name="Город", max_length=100)
    photo = models.ImageField(
        verbose_name="Фотография пользователя",
        default="nofoto.png",
        upload_to=img_directory_path
    )

    def save(self, *args, **kwargs):
        super().save()
        photo_root = Image.open(self.photo.path)
        if photo_root.width > 200 and photo_root.height > 200:
            new_size = (200, 200)
            photo_root.thumbnail(new_size)
            photo_root.save(self.photo.path)

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class CarAdvertisement(models.Model):
    """Модель для обьявления по продаже авто"""

    fuel_variant = (
        ('Н', 'Не указан'),
        ('Д', 'Дизель'),
        ('Б', 'Бензин'),
        ('ГБ', 'Газ/Бензин'),
        ('Е', 'Електро'),
        ('Г', 'Гибрид'),
    )
    transmission_variant = (
        ('Н', 'Не указан'),
        ('М', 'Механика'),
        ('А', 'Автомат'),
        ('В', 'Вариатор'),
        ('Т', 'Типтроник'),
        ('Ад', 'Адаптивная '),
    )

    typeauto = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="typeauto", verbose_name="Тип кузова", null=True
    )
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="authoradd", verbose_name="Автор"
    )
    brand = models.CharField(
        max_length=100, verbose_name="Марка"
    )
    model_car = models.CharField(
        max_length=100, verbose_name="Модель")

    engine_volume = models.FloatField(
        verbose_name="Обьём двигателя"
    )
    fuel = models.CharField(
        max_length=3, verbose_name="Топливо", choices=fuel_variant, blank=True, default="Н"
    )
    transmission = models.CharField(
        max_length=3, verbose_name="Трансмиссия", choices=transmission_variant, blank=True, default="Н"
    )
    color = models.CharField(
        max_length=100, verbose_name="Цвет"
    )
    odometr = models.PositiveIntegerField(verbose_name="Пробег")
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    price = models.PositiveIntegerField(verbose_name="Цена")
    city = models.CharField(
        max_length=100, verbose_name="Город регистрации"
    )
    header = models.CharField(
        max_length=250, verbose_name="Заголовок", unique=True
    )
    description = models.TextField(verbose_name="Описание")
    add_params = models.JSONField(verbose_name="Дополнителные параметры")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.author} -> {self.brand}"

    def get_absolute_url(self):
        return reverse("detail-advertisement", args=[str(self.id)])

    class Meta:
        verbose_name = 'Обьявление'
        verbose_name_plural = 'Обьявления'


class ImageCars(models.Model):
    """Модель для изображений авто"""
    title = models.CharField(
        verbose_name="Фотография авто", max_length=100, default="Фото атомобиля"
    )
    image = models.ImageField(
        upload_to="photo-cars",
        default="car_no.jpg",
        verbose_name="Фотографии автомобиля"
    )
    image2 = models.ImageField(
        upload_to="photo-cars",
        default="car_no.jpg",
        verbose_name="Фотографии автомобиля"
    )
    image3 = models.ImageField(
        upload_to="photo-cars",
        default="car_no.jpg",
        verbose_name="Фотографии автомобиля"
    )
    image4 = models.ImageField(
        upload_to="photo-cars",
        default="car_no.jpg",
        verbose_name="Фотографии автомобиля"
    )
    image5 = models.ImageField(
        upload_to="photo-cars",
        default="car_no.jpg",
        verbose_name="Фотографии автомобиля"
    )
    image6 = models.ImageField(
        upload_to="photo-cars",
        default="car_no.jpg",
        verbose_name="Фотографии автомобиля"
    )
    car = models.ForeignKey(
        CarAdvertisement,
        on_delete=models.CASCADE,
        verbose_name="Обьявление"
    )

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(args, kwargs)
        photo_root = Image.open(self.image.path)
        if photo_root.width > 1200 or photo_root.height > 1200:
            new_size = (photo_root.width * 0.7, photo_root.height * 0.7)
            photo_root.thumbnail(new_size)
            photo_root.save(self.image.path)

    class Meta:
        verbose_name = "Фотография автомобиля"
        verbose_name_plural = "Фотографии автомобилей"
