# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    try:
        return f"{(float(value) / float(total) * 100):.0f}"  # rounded percentage without decimals
    except (ValueError, ZeroDivisionError):
        return "0"
