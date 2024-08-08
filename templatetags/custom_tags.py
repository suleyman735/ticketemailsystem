
# templatetags/functions.py

from django import template
register = template.Library()
@register.simple_tag
def calculate_active(value1, value2):
    try:
        active_tickets, closed_tickets = value1, value2
        result = (value1 + value2) / 100 * value1
        return result * 100
    except (ValueError, TypeError):
        return 0