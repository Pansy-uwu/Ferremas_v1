from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def div(value, arg):
    try:
        value = Decimal(value)
        arg = Decimal(arg)
        result = value / arg
        return f"{result:.2f}"  # Formatear el resultado con 2 decimales
    except (ValueError, InvalidOperation, ZeroDivisionError):
        return None

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)