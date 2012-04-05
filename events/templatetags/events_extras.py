from django import template
from django.conf import settings

register = template.Library()

@register.filter
def default_picture(value):
  """Returns a default value if string does not exist"""
  if value == None:
     return settings.DEFAULT_PICTURE
  return value
