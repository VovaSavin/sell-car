from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Category,
    CarAdvertisement,
    # CustomUser,
    ImageCars,
    MyUser
)
from django.contrib.auth.admin import UserAdmin


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("body",)


# @admin.register(MyUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone", "photo_get", 'is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Info'), {'fields': ('phone', 'city', 'photo')}),
    )
    list_filter = ("username", "email", "phone",)

    def photo_get(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="20" height="25">')

    photo_get.short_description = "Фото пользователя"


@admin.register(CarAdvertisement)
class CarAdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "brand", "model_car", "author", "typeauto",
    )
    list_filter = (
        "typeauto", "author", "brand", "model_car"
    )


@admin.register(ImageCars)
class ImageCarsAdmin(admin.ModelAdmin):
    list_display = ("title", "get_image")

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="20" height="25">')

    get_image.short_description = "Фото авто"


admin.site.register(MyUser, CustomUserAdmin)
