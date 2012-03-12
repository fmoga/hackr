from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.forms import ModelForm, Textarea, ChoiceField
from django.forms.widgets import RadioSelect
from django import forms
from django.db import models
from decorators import check_login
from django.core.urlresolvers import reverse
from events.models import Hackathon, Project, PollOption
from datetime import datetime
from pprint import pprint

def login(request):
  return render_to_response('login.html', {}, RequestContext(request))

def login_error(request):
  return render_to_response('login-error.html', {}, RequestContext(request))

@check_login()
def index(request):
  hackathons = Hackathon.objects.filter(deleted=False)
  in_future = []
  in_progress = []
  completed = []
  for hack in hackathons:
    if hack.state == Hackathon.COMPLETED:
      completed.append(hack)
    elif hack.start > datetime.now():
      in_future.append(hack)
    else:
      in_progress.append(hack)
      
  return render_to_response('index.html', {'hackathons': in_progress + in_future + completed, 'current_datetime': datetime.now()}, RequestContext(request))
 
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
  return render_to_response('event.html', {'hack': hack, 'projects': projects, 'form': form, 'comment_form_excludes': ['name', 'url', 'email', 'honeypot']} , RequestContext(request))

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
    return HttpResponseForbidden('<h1>Forbidden - Only event author can perform changes</h1>')
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
    return HttpResponseForbidden('<h1>Forbidden - Only event author can perform changes</h1>')
  event.deleted = True
  event.save()
  return HttpResponseRedirect(reverse('events.views.index'))

@check_login()
def event_state(request, event_id):
  event = get_object_or_404(Hackathon, pk=event_id)
  if not event.creator == request.user:
    return HttpResponseForbidden('<h1>Forbidden - Only event author can perform changes</h1>')
  if not event.state == Hackathon.COMPLETED:
    event.state += 1
    event.save()
  return HttpResponseRedirect(reverse('events.views.event', args=[event.id]))

@check_login()
def event_poll(request, event_id):
  event = get_object_or_404(Hackathon, pk=event_id)
  if event.state == Hackathon.VOTING:
    return render_to_response('poll.html', {'event': event},  RequestContext(request))
  elif event.state == Hackathon.COMPLETED:
    return render_to_response('poll.html', {'event': event},  RequestContext(request))
  return HttpResponseNotFound('<h1>Poll Not Found</h1>')

@check_login()
def vote(request, event_id):
  event = get_object_or_404(Hackathon, pk=event_id)
  if event.state != event.VOTING:
    return HttpResponseForbidden('<h1>Forbidden - Vote is not running</h1>')
  if request.user in event.voters.all():
    return HttpResponseForbidden('<h1>Forbidden - You already voted</h1>')
  option_id = request.POST['option']  
  if option_id == '-1':
    # new proposal
    proposal = request.POST['proposal']
    new_option = PollOption(event=event, text=proposal, count=1)
    new_option.save()
  else:
    # existing option
    option = get_object_or_404(PollOption, pk=option_id)
    print option.text
    if option.event == event:
      option.count += 1 
      option.save()
    else:
      return HttpResponseBadRequest('<h1>Bad Request - Option does not belong to poll</h1>')
  event.voters.add(request.user)
  return HttpResponseRedirect(reverse('events.views.event_poll', args=[event.id]))

@check_login()
def edit_project(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if not project.creator == request.user:
    return HttpResponseForbidden('<h1>Forbidden - Only project author can perform changes</h1>')
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
    return HttpResponseForbidden('<h1>Forbidden - Only project author can perform changes</h1>')
  project.deleted = True
  project.save()
  return HttpResponseRedirect(reverse('events.views.event', args=[project.event.id]))

@check_login()
def join_project(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if not request.user in project.hackers.all():
    project.hackers.add(request.user)
    project.save()
  return HttpResponseRedirect(reverse('events.views.event', args=[project.event.id]))

@check_login()
def leave_project(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if request.user in project.hackers.all():
    project.hackers.remove(request.user)
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
