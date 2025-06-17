from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value, total):
    try:
        value = float(value)
        total = float(total)
        if total == 0:
            return "0%"
        return f"{(value / total) * 100:.2f}%"
    except (ValueError, ZeroDivisionError):
        return ""
