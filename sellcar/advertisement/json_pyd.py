from pydantic import BaseModel


class AdditionalParametrs(BaseModel):
    """Клас для отображения доп параметров в CarAdvertisement"""
    Electricalpackage: int
    # Допиши вывод всех доп параметров
    # Словарь с переводом всех доп параметров {англ: руск}
