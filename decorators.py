from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from functools import wraps

def check_login():
  def decorator(func):
    def inner_decorator(request, *args, **kwargs):
      if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
      return func(request, *args, **kwargs)
    return wraps(func)(inner_decorator)
  return decorator
