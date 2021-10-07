from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import (
    MyUser,
    CarAdvertisement,
    Category,
    ImageCars
)
from .forms import (
    CarAdvertisementForm,
    ImageCarsForm,
    EditMyUser,
)
from .filter import CarAdvertisementFilter
from .helper import get_adds, get_paginate


# Create your views here.


# Добавление и редактирование доп параметров через Pydantic


class GetBodycar:
    """Выводит список всех типов кузова автомобиля"""

    @staticmethod
    def get_body():
        return Category.objects.all()


class Messages:
    """Класс для вывода сообщений"""

    @property
    def success_message(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class ListAdv(GetBodycar, ListView):
    """Список всех обьявлений на сайте"""
    model = CarAdvertisement
    template_name = "advertisement/cars.html"
    context_object_name = "filters"
    paginate_by = 6

    def get_queryset(self):
        return CarAdvertisementFilter(
            self.request.GET,
            CarAdvertisement.objects.all()
        ).qs

    def get_context_data(self, **kwargs):
        context = super(ListAdv, self).get_context_data(**kwargs)
        context["title"] = "Все обьявления"
        context["additions"] = get_adds()
        context["response"] = get_paginate(
            self.get_queryset(),
            self.paginate_by,
            self.request,
        )
        context["filter"] = CarAdvertisementFilter(
            self.request.GET,
            CarAdvertisement.objects.all(),
        )
        return context


class DetailAdv(DetailView):
    """Детальный вывод обьявления"""
    model = CarAdvertisement
    template_name = "advertisement/detail-advertisement.html"
    context_object_name = "advertisement"

    def get_context_data(self, **kwargs):
        context = super(DetailAdv, self).get_context_data(**kwargs)
        context["title"] = CarAdvertisement.objects.get(
            id=self.kwargs['pk']
        )
        context["additions"] = get_adds()
        return context


class MyAdvertisement(LoginRequiredMixin, GetBodycar, ListView):
    """Вывод вcех своих обьявлений"""
    model = CarAdvertisement
    template_name = "advertisement/cars.html"
    context_object_name = "filters"
    paginate_by = 6

    def get_queryset(self):
        return CarAdvertisementFilter(
            self.request.GET,
            CarAdvertisement.objects.filter(author=self.request.user)
        ).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мои обьявления"
        context["filter"] = CarAdvertisementFilter(
            self.request.GET,
            CarAdvertisement.objects.filter(
                author=self.request.user
            ),
        )
        context["response"] = get_paginate(
            self.get_queryset(),
            self.paginate_by,
            self.request,
        )
        context["additions"] = get_adds()
        return context


class UserAdvertisement(GetBodycar, ListView):
    """Вывод обьявлений от конкретного пользователя"""
    model = CarAdvertisement
    template_name = "advertisement/cars.html"
    context_object_name = "filters"
    paginate_by = 6

    def get_queryset(self):
        return CarAdvertisementFilter(
            self.request.GET, CarAdvertisement.objects.filter(
                author=self.kwargs.get("pkuser")
            )
        ).qs

    def get_context_data(self, **kwargs):
        context = super(UserAdvertisement, self).get_context_data(**kwargs)
        context["title"] = f"Обьявления {MyUser.objects.get(username=self.kwargs.get('author'))}"
        context["filter"] = CarAdvertisementFilter(
            self.request.GET,
            CarAdvertisement.objects.filter(
                author=self.kwargs.get("pkuser")
            ),
        )
        context["response"] = get_paginate(
            self.get_queryset(),
            self.paginate_by,
            self.request,
        )
        context["additions"] = get_adds()
        return context


class CreateAdv(Messages, LoginRequiredMixin, CreateView):
    """Создание обьявления"""
    model = CarAdvertisement
    form_class = CarAdvertisementForm
    success_url = "/"
    template_name = "advertisement/create.html"
    prefix = 'ad'
    success_message = "Обьявление опубликовано!"

    def img_form_valid(self):
        img_form = ImageCarsForm(
            self.request.POST,
            self.request.FILES,
            prefix='img'
        )
        if img_form.is_valid():
            object_img = img_form.save(commit=False)
            object_img.car = self.object
            object_img.save()
        else:
            print("Bad")

    def form_valid(self, form):
        form.instance.author = MyUser.objects.get(
            username=self.request.user
        )
        add = self.request.POST.getlist("additional")
        new_add = {
            "Luke": 0, "Multifunc": 0,
            "Parktronic": 0, "conditioner": 0,
            "Sensorlight": 0, "Sensorrain": 0,
            "Electricalpackage": 0, "Leatherinterior": 0,
            "headlightwasher": 0, "heatedsteeringwheel": 0,
            "Cruisecontrol": 0, "Powerstiring": 0,
            "Startbutton": 0, "Climatcontrol": 0,
            "heatedmirrors": 0, "Safesystem": 0,
            "Heatedseats": 0, "Onboardcomputer": 0,
            "Electricwindows": 0
        }
        for self.x in add:
            new_add[self.x] = 1

        form.instance.add_params = new_add
        self.object = form.save()
        self.img_form_valid()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateAdv, self).get_context_data(**kwargs)
        context["title"] = "Создать обьявление"
        context["img_form"] = ImageCarsForm(prefix='img')
        return context


class UpdateAdv(UserPassesTestMixin, Messages, UpdateView):
    model = CarAdvertisement
    form_class = CarAdvertisementForm
    template_name = "advertisement/update-adv.html"
    prefix = 'ad'
    success_message = "Объявление успешно обновлено!"

    def test_func(self):
        advert = self.get_object()
        if self.request.user == advert.author:
            return True
        return False

    def img_form_valid(self):
        img_form = ImageCarsForm(
            self.request.POST,
            self.request.FILES,
            prefix='img',
            instance=ImageCars.objects.get(car_id=self.kwargs["pk"])
        )
        if img_form.is_valid():
            object_img = img_form.save(commit=False)
            object_img.car = self.object
            object_img.save()

    def form_valid(self, form):
        form.instance.author = MyUser.objects.get(
            username=self.request.user
        )
        add = self.request.POST.getlist("additional")
        print(add)
        new_add = {
            "Luke": 0, "Multifunc": 0,
            "Parktronic": 0, "conditioner": 0,
            "Sensorlight": 0, "Sensorrain": 0,
            "Electricalpackage": 0, "Leatherinterior": 0,
            "headlightwasher": 0, "heatedsteeringwheel": 0,
            "Cruisecontrol": 0, "Powerstiring": 0,
            "Startbutton": 0, "Climatcontrol": 0,
            "heatedmirrors": 0, "Safesystem": 0,
            "Heatedseats": 0, "Onboardcomputer": 0,
            "Electricwindows": 0
        }
        for self.x in add:
            if self.x in new_add:
                new_add[self.x] = 1
        print(new_add)
        form.instance.add_params = new_add
        self.object = form.save()
        self.img_form_valid()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(UpdateAdv, self).get_context_data(**kwargs)
        context["title"] = f"Редактирование обьявление {self.get_object().brand} "
        context["img_form"] = ImageCarsForm(
            prefix="img",
            instance=ImageCars.objects.get(car_id=self.kwargs["pk"])
        )
        context["adds"] = get_adds()
        return context


class EditUser(Messages, LoginRequiredMixin, UpdateView):
    """Редактирование данных о пользователе"""
    model = MyUser
    form_class = EditMyUser
    template_name = "advertisement/edit-user.html"
    slug_field = "username"
    slug_url_kwarg = 'username'
    success_url = "/"
    success_message = "Информация успешно обновлена!"

    def get_context_data(self, **kwargs):
        context = super(EditUser, self).get_context_data(**kwargs)
        context["title"] = "Редактирование профиля"
        return context


def rules(request):
    """
    Правила сайта
    :param request:
    :return:
    """
    context = {
        "title": "Правила сайта"
    }
    return render(request, "advertisement/rules.html", context)


def about(request):
    """
    Прочая информация
    :param request:
    :return:
    """
    context = {
        "title": "О нас"
    }
    return render(request, "advertisement/about.html", context)


def support(request):
    """
    Прочая информация
    :param request:
    :return:
    """
    context = {
        "title": "Попробуйте связаться"
    }
    return render(request, "advertisement/contact.html", context)
