from django import template
from advertisement.forms import ImageCarsForm

register = template.Library()


@register.inclusion_tag("advertisement/tag/image-form.html")
def get_imageForm():
    """Возвращает форму добавления фото автомобилей"""
    return {"img_form": ImageCarsForm()}
