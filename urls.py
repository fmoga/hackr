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
)

urlpatterns += patterns('',
  url(r'', include('social_auth.urls')),
)
