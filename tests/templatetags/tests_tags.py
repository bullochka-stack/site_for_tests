# создание пользовательких тегов
from django import template

from tests.models import Categories

register = template.Library()


# simple тег для получения категорий
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Categories.objects.all()


# inclusion тег для получения и показа категорий
@register.inclusion_tag('tests/list_categories.html')
def show_categories():
    categories = Categories.objects.all()
    return {'categories': categories, }
