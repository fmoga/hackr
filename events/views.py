from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from decorators import check_login
from django.core.urlresolvers import reverse
from events.models import Hackathon
from pprint import pprint

def login(request):
  return render_to_response('login.html', {}, RequestContext(request))

def login_error(request):
  return render_to_response('login-error.html', {}, RequestContext(request))

@check_login()
def index(request):
  hackathons = Hackathon.objects.all()
  return render_to_response('index.html', {'hackathons': hackathons}, RequestContext(request))
 
@check_login()
def logout(request):
  auth_logout(request)
  return HttpResponseRedirect(reverse('events.views.login'))

@check_login()
def event(request, event_id):
  hack = get_object_or_404(Hackathon, pk=event_id)
  return render_to_response('event.html', {'hack': hack} , RequestContext(request))

def add_event(request):
  # TODO
  return HttpResponseNotFound('<h1>Not Yet Implemented</h1>')

@check_login()
def edit_event(request, event_id):
  # TODO
  return HttpResponseNotFound('<h1>Not Yet Implemented</h1>')

@check_login()
def delete_event(request, event_id):
  # TODO
  return HttpResponseNotFound('<h1>Not Yet Implemented</h1>')
