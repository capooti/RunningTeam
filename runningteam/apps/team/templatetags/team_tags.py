from django import template
from team.models import Runner, Race, RaceRunner
from datetime import *

register = template.Library()

# best races
def best_races(racetype, gender):
    """
    Best races given a racetype and a gender.
    """
    idlist = []
    runneridlist = []
    for i in range(1, 6): # only first 5 ones TODO parametrize this value
        rr = RaceRunner.objects.filter(race__racetype__name=racetype, 
            time__gte=time(0,0,0), runner__gender=gender).exclude(
            runner__id__in=runneridlist).order_by('time')[:1]
        if rr.count() > 0:
            idlist = idlist + [rr[0].id]
            runneridlist = runneridlist + [rr[0].runner.id]
    best_races = RaceRunner.objects.filter(id__in=idlist).order_by('time')
    return best_races

def best_results(racetype, gender):
    """
    Inclusion tag for best races, given a racetype and a gender.
    """
    records = best_races(racetype, gender)
    return {
        'records': records
    }
register.inclusion_tag('team/inc_records.html')(best_results)

def best_results_runner(runner, racetype):
    """
    Inclusion tag for best results, given a runner and a racetype.
    """
    records = RaceRunner.objects.filter(race__racetype__name=racetype, time__gte=time(0,0,0), runner__id=runner.id).order_by('time')[:5]
    return {
        'records': records,
        'display_runner': True,
        'display_racetype': True
    }
register.inclusion_tag('team/inc_records.html')(best_results_runner)

def races_list(limit=1000):
    """
    Inclusion tag for listing all races.
    """
    races = Race.objects.filter(date__lte=datetime.now()).order_by('-date')[:limit]
    return {
        'races': races
    }
register.inclusion_tag('team/inc_races.html')(races_list)

def future_races_list(runner=None, limit=1000):
    """
    Inclusion tag for listing all future races, eventually given a runner.
    """
    future_races = Race.objects.filter(date__gte=datetime.now()).order_by('-date')[:limit]
    future_races.subscribable = False
    if runner:
        future_races.subscribable = True
        for race in future_races:
          racerunner = race.racerunner_set.filter(runner__id=runner.id)
          race.subscribed = False
          if racerunner.count() > 0:
            race.subscribed = True
    from django.conf import settings
    return {
        'future_races': future_races,
        'media_url': settings.MEDIA_URL
    }
register.inclusion_tag('team/inc_future_races.html')(future_races_list)

