from django import template

register = template.Library()


@register.filter(name='calculate_sub')
def calculate_sub(price, quantity):
    """
    Function to recalculate product prices from quantity changes.
    """
    return price * quantity
