from django import template
register = template.Library()

@register.filter(name="veri")
def veri(valeur):
    return str(valeur)


