from django import template

register = template.Library()

@register.filter()
def rangelist(min=5):
    return range(min)