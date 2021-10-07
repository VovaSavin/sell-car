import django_filters
from .models import CarAdvertisement
from django import forms
from .helper import (
    get_fuels,
    get_transmissions,
    get_body_cars,
)


class CustomNumberFilter(django_filters.NumberFilter):
    field_class = forms.IntegerField


class CharFilterIn(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class CarAdvertisementFilter(django_filters.FilterSet):
    """
    Фильтры для обьявлений.
    Название полей для фильтрации указывать такие же как и models.py
    """

    brand = django_filters.CharFilter(lookup_expr='icontains')
    model_car = django_filters.CharFilter(lookup_expr='icontains')
    header = django_filters.CharFilter(lookup_expr='icontains')
    fuel = django_filters.ChoiceFilter(choices=get_fuels(), empty_label="Не выбран")
    transmission = django_filters.ChoiceFilter(choices=get_transmissions(), empty_label="Не выбран")
    typeauto = django_filters.ChoiceFilter(choices=get_body_cars(), empty_label="Не выбран")
    add_params = CharFilterIn(field_name='add_params', method='filter_params')

    odometr = CustomNumberFilter()
    odometr__gte = CustomNumberFilter(
        field_name="odometr",
        lookup_expr='gte'
    )
    odometr__lte = CustomNumberFilter(
        field_name="odometr",
        lookup_expr='lte'
    )

    year = CustomNumberFilter()
    year__gte = CustomNumberFilter(
        field_name="year",
        lookup_expr='gte'
    )
    year__lte = CustomNumberFilter(
        field_name="year",
        lookup_expr='lte'
    )

    price = CustomNumberFilter()
    price__gte = CustomNumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    price__lte = CustomNumberFilter(
        field_name='price',
        lookup_expr='lte'
    )

    def filter_params(self, queryset, name, value):
        # construct the full lookup expression.
        q = {f'add_params__{k}': 1 for k in value}
        return queryset.filter(**q)

    class Meta:
        model = CarAdvertisement
        fields = [
            "brand",
            "model_car",
            "header",
            "fuel",
            "transmission",
            "typeauto",
            "add_params",
        ]
