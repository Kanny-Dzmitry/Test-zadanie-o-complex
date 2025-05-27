from django import template

register = template.Library()

@register.filter
def get_item(list_obj, index):
    """Возвращает элемент списка по индексу"""
    try:
        return list_obj[index]
    except (IndexError, TypeError):
        return None 