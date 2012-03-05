from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from decorators import check_login
from django.core.urlresolvers import reverse
from pprint import pprint

def login(request):
  return render_to_response('login.html', {}, RequestContext(request))

def login_error(request):
  return render_to_response('login-error.html', {}, RequestContext(request))

@check_login()
def index(request):
  return render_to_response('index.html', {}, RequestContext(request))
 
@check_login()
def logout(request):
  auth_logout(request)
  return HttpResponseRedirect(reverse('events.views.login'))
