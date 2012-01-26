from django.conf.urls.defaults import *
from team.models import Race

urlpatterns = patterns('',
    url(r'^$', 'team.views.home', 
        name="home"),
    url(r'^runners/list', 'team.views.runners_list', 
        name="runners-list"),
    url(r'^runners/(?P<runner_id>\d+)/$', 'team.views.runner_details', 
        name="runner-details"),
    url(r'^runners/update', 'team.views.runner_update', 
        name='runner-update'),
    url(r'^races/future', 'team.views.future_races_list', 
        name='future-races'),
    url(r'^races/(?P<race_id>\d+)/details$', 'team.views.race_details', 
        name="race-details"),
    url(r'^races/subscribe/(?P<race_id>\d+)/$', 'team.views.race_subscribe', 
        name='race-subscribe'),
    url(r'^races/photos/(?P<race_id>\d+)/add$', 'team.views.race_photo_add', 
        name='race-photo-add'),
    # stats
    url(r'^stats', 'team.views.stats', name="stats"),
    # about page
    url(r'^about', 'team.views.about', name="about"),
    # auth pages
    url(r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'team/auth/login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'template_name': 'team/auth/logout.html'}, name="logout"),
    url(r'^login/$', 'django.contrib.auth.views.password_change', 
        {'template_name': 'team/auth/password_change.html'}, 
        name="password-change"),
)

gare_dict = {
    'queryset': Race.objects.all(), 
    'date_field': 'date',
    'num_latest': 1000,
    'template_name':'team/race/archive/race_archive.html',
}

gare_dict_year = {
    'queryset': Race.objects.all(), 
    'date_field': 'date',
    'make_object_list': 'True',
    'allow_empty': 'True',
    'template_name':'team/race/archive/race_archive_year.html',
}

gare_dict_month = {
    'queryset': Race.objects.all().order_by('-date'), 
    'date_field': 'date',
    'month_format': '%m',
    'template_name':'team/race/archive/race_archive_month.html',
}

urlpatterns += patterns('django.views.generic.date_based',
        url(r'^races/archive/(?P<year>\d{4})/(?P<month>\d{2})/$', 
            'archive_month', gare_dict_month, name='race-archive-month'),
        url(r'^races/archive/(?P<year>\d{4})/$', 
            'archive_year', gare_dict_year, name='race-archive-year'),
        url(r'^races/archive$', 
            'archive_index', gare_dict, name='race-archive'),
    )


