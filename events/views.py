from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from events.models import HackrUser
from decorators import check_login
from pprint import pprint

def login(request):
  return render_to_response('login.html', {}, RequestContext(request))

def login_error(request):
  return render_to_response('login-error.html', {}, RequestContext(request))

@check_login()
def index(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/login/?next=%s' % request.path)
  logged_user = HackrUser.objects.get(google_id=request.user.first_name)
  return render_to_response('index.html', {'logged_user': logged_user}, RequestContext(request))
 
@check_login()
def logout(request):
  auth_logout(request)
  return HttpResponseRedirect('/')
