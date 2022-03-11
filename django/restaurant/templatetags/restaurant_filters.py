from django import template
import os


register = template.Library()

@register.filter(name='get_extension')
def get_extension(file):
    name, extension = os.path.splitext(file.name)
    return extension[1:]