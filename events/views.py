from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.forms import ModelForm, Textarea
from django import forms
from django.db import models
from decorators import check_login
from django.core.urlresolvers import reverse
from events.models import Hackathon, Project
from pprint import pprint

def login(request):
  return render_to_response('login.html', {}, RequestContext(request))

def login_error(request):
  return render_to_response('login-error.html', {}, RequestContext(request))

@check_login()
def index(request):
  hackathons = Hackathon.objects.filter(deleted=False)
  return render_to_response('index.html', {'hackathons': hackathons}, RequestContext(request))
 
@check_login()
def logout(request):
  auth_logout(request)
  return HttpResponseRedirect(reverse('events.views.login'))

@check_login()
def event(request, event_id):
  hack = get_object_or_404(Hackathon, pk=event_id)
  projects = hack.project_set.filter(deleted=False)
  if request.method == 'POST':
    form = ProjectForm(request.POST, label_suffix='')
    if form.is_valid():
      new_project = form.save(commit=False)
      new_project.creator = request.user
      new_project.event = hack
      new_project.save()
      return HttpResponseRedirect(reverse('events.views.event', args=[event_id]))
  else:
    form = ProjectForm(label_suffix='')
  return render_to_response('event.html', {'hack': hack, 'projects': projects, 'form': form} , RequestContext(request))

@check_login()
def add_event(request):
  if request.method == 'POST':
    form = EventForm(request.POST, label_suffix='')
    if form.is_valid():
      new_event = form.save(commit=False)
      new_event.creator = request.user
      new_event.save()
      return HttpResponseRedirect(reverse('events.views.index'))
  else:
    form = EventForm(label_suffix='')
  return render_to_response('add_event.html', {'form': form},  RequestContext(request))

@check_login()
def edit_event(request, event_id):
  event = get_object_or_404(Hackathon, pk=event_id)
  if not event.creator == request.user:
    return HttpResponseForbidden()
  if request.method == 'POST':
    form = EventForm(request.POST, instance=event, label_suffix='')
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('events.views.index'))
  else:
    form = EventForm(instance=event, label_suffix='')
  return render_to_response('edit_event.html', {'form': form, 'event': event},  RequestContext(request))

@check_login()
def delete_event(request, event_id):
  event = get_object_or_404(Hackathon, pk=event_id)
  if not event.creator == request.user:
    return HttpResponseForbidden()
  event.deleted = True
  event.save()
  return HttpResponseRedirect(reverse('events.views.index'))

@check_login()
def edit_project(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if not project.creator == request.user:
    return HttpResponseForbidden()
  if request.method == 'POST':
    form = ProjectForm(request.POST, instance=project, label_suffix='')
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('events.views.event', args=[project.event.id]))
  else:
    form = ProjectForm(instance=project, label_suffix='')
  return render_to_response('edit_project.html', {'form': form, 'project': project},  RequestContext(request))

@check_login()
def delete_project(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if not project.creator == request.user:
    return HttpResponseForbidden()
  project.deleted = True
  project.save()
  return HttpResponseRedirect(reverse('events.views.event', args=[project.event.id]))

# Forms
 
class EventForm(ModelForm):
  # specify the custom format and jquery ui class for the datetime field
  start = forms.DateTimeField(('%d %B %Y, %I%p',), widget=forms.DateTimeInput(attrs={'class':'datePicker', 'readonly':'true'}, format='%d %B %Y, %I%p'))
  class Meta:
    model=Hackathon
    fields = ('title', 'description', 'start', 'location')
    widgets = {
      'description': Textarea(attrs={'rows': 3}),
    }

class ProjectForm(ModelForm):
  class Meta:
    model=Project
    fields = ('title', 'description')
    widgets = {
      'description': Textarea(attrs={'rows': 3}),
    }
