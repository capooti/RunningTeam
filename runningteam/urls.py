from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'team.views.home', name="home"),
    url(r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('threadedcomments.urls')),
    (r'^photos/', include('photos.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^team/', include('team.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
