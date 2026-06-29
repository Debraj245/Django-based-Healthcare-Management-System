from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except:
        return value

@register.filter
def split(value, sep):
    return value.split(sep)
