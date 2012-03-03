from django.db import models

class HackrUser(models.Model):
  google_id = models.CharField(primary_key=True, max_length=30)
  first_name = models.CharField(max_length=50, null=True)
  last_name = models.CharField(max_length=50, null=True)
  full_name = models.CharField(max_length=100, null=True)
  email = models.EmailField()
  profile = models.CharField(max_length=200, null=True)
  picture = models.CharField(max_length=200, null=True)

  def __unicode__(self):
    return self.full_name

class Hackathon(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  start = models.DateTimeField()
  finish = models.DateTimeField()

class Project(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  creator = models.ForeignKey(HackrUser, related_name='created_projects')
  event = models.ForeignKey(Hackathon)
  hackers = models.ManyToManyField(HackrUser, related_name='joined_projects')

class Comment(models.Model):
  text = models.TextField()
  project = models.ForeignKey(Project)
  creator = models.ForeignKey(HackrUser)
