from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('events.views',
  url(r'^$', 'index'),
  url(r'^login/$', 'login'),
  url(r'^logout/$', 'logout'),
  url(r'^login-error/$', 'login_error'),
  url(r'^event/add/$', 'add_event'),
  url(r'^event/(?P<event_id>\d+)/edit/$', 'edit_event'),
  url(r'^event/(?P<event_id>\d+)/delete/$', 'delete_event'),
  url(r'^event/(?P<event_id>\d+)/$', 'event'),
  url(r'^project/(?P<project_id>\d+)/edit/$', 'edit_project'),
  url(r'^project/(?P<project_id>\d+)/delete/$', 'delete_project'),
  url(r'^project/(?P<project_id>\d+)/join/$', 'join_project'),
  url(r'^project/(?P<project_id>\d+)/leave/$', 'leave_project'),
)

urlpatterns += patterns('',
  url(r'', include('social_auth.urls')),
)
