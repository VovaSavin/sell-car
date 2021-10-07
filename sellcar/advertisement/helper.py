from .models import Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_adds() -> dict:
    """Возвращает словарь перевода доп параметров с англ-руск"""
    add = {
        "Electricalpackage": "Електропакет",
        "Electricwindows": "Електростеклоподъёмники",
        "conditioner": "Кондиционер",
        "Safesystem": "Охранная система",
        "Parktronic": "Парктроник",
        "Onboardcomputer": "Бортовой компьютер",
        "Sensorlight": "Датчик света",
        "Startbutton": "Запуск с кнопки",
        "Climatcontrol": "Климат контроль",
        "Leatherinterior": "Кожанный салон",
        "Cruisecontrol": "Круиз контроль",
        "Luke": "Люк",
        "Multifunc": "Мультируль",
        "headlightwasher": "Омыватель фар",
        "heatedmirrors": "Подогрев зеркал",
        "heatedsteeringwheel": "Подогрев руля",
        "Sensorrain": "Сенсор дождя",
        "Powerstiring": "Усилитель руля",
        "Heatedseats": "Подогрев сидений",
    }
    return add


def get_fuels() -> tuple:
    """Кортеж кортежей видов топлива для select in html"""
    fuels = (
        ('Д', 'Дизель'),
        ('Б', 'Бензин'),
        ('ГБ', 'Газ/Бензин'),
        ('Е', 'Електро'),
        ('Г', 'Гибрид'),
    )
    return fuels


def get_transmissions() -> tuple:
    """Кортеж кортежей трансмиссий для select in html"""
    transmissions = (
        ('М', 'Механика'),
        ('А', 'Автомат'),
        ('В', 'Вариатор'),
        ('Т', 'Типтроник'),
        ('Ад', 'Адаптивная '),
    )
    return transmissions


def get_body_cars() -> list:
    """Список кортежей кузовов авто"""
    body = []
    y = 1
    for x in Category.objects.all():
        body.append(
            (y, x)
        )
        y += 1
    return body


def get_paginate(object_list, per_page, request):
    """
    Создаёт обьект класса пагинатора
    и возвращает ответ
    """
    paginator = Paginator(object_list, per_page)
    page = request.GET.get("page")

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return response
    # return  paginator
