from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from social_auth.signals import pre_update
from events.googlebackend import GoogleProfileBackend
from pprint import pprint

# Models

class UserProfile(models.Model):
  # required field for django user profiles
  user = models.OneToOneField(User)
  # custom fields
  google_id = models.CharField(max_length=30, null=True)
  full_name = models.CharField(max_length=100, null=True)
  profile = models.CharField(max_length=200, null=True)
  picture = models.CharField(max_length=200, null=True)

  def __unicode__(self):
    if self.full_name:
      return u'%s' % self.full_name
    return self.user.username

class Hackathon(models.Model):
  RUNNING = 0
  VOTING = 1
  COMPLETED = 2
  title = models.CharField(max_length=100)
  description = models.TextField()
  start = models.DateTimeField(verbose_name='When')
  location = models.CharField(max_length=200, verbose_name='Where')
  creator = models.ForeignKey(User)
  state = models.IntegerField(default=0)

  def __unicode__(self):
    return u'%s' % self.title

class Project(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  creator = models.ForeignKey(User, related_name='created_projects')
  event = models.ForeignKey(Hackathon)
  hackers = models.ManyToManyField(User, related_name='joined_projects')

# Signals for models

def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

def google_extra_values(sender, user, response, details, **kwargs):
  profile = user.get_profile()
  profile.google_id = response.get('id')
  profile.full_name = response.get('name')
  profile.picture = response.get('picture')
  profile.profile = response.get('link')
  pprint(vars(profile))
  profile.save()
  return True

pre_update.connect(google_extra_values, sender=GoogleProfileBackend)
