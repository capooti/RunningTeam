# -*- coding: utf-8 -*-

from datetime import *

# django
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import modelformset_factory

# photos
from photos.forms import PhotoUploadForm
from photos.models import Image, Pool

# team
from team.models import Runner, Race, RaceRunner, RaceType, RunnerForm

# best races
def best_races(tipogara, sesso='M'):
  idlist = []
  atletaidlist = []
  for i in range(1, 11):
	  # seleziono posizione i
	  ga = GaraAtleta.objects.filter(gara__tipogara__nome=tipogara, tempo__gte=time(0,0,0), atleta__sesso=sesso).exclude(atleta__id__in=atletaidlist).order_by('tempo')[:1]
	  if ga.count() > 0:
	    idlist = idlist + [ga[0].id]
	    atletaidlist = atletaidlist + [ga[0].atleta.id]
	# restitutisco i migliori risultati
  best = GaraAtleta.objects.filter(id__in=idlist).order_by('tempo')
  return best

# about
def about(request):
    return render_to_response("team/about.html", {
    }, context_instance=RequestContext(request))

# stats
def stats(request):
    return render_to_response("team/stats.html", {
    }, context_instance=RequestContext(request))
    
# home page
def home(request):
    race_maintypes = RaceType.objects.all().filter(is_maintype=True)
    future_races = Race.objects.filter(date__gte=datetime.now()).order_by('-date')
    user = request.user
    runner = None
    if user.is_authenticated():
        runner = user.get_runner()
        runnerid = runner.id
        for race in future_races:
            racerunner = race.racerunner_set.filter(runner__id=runnerid)
            race.subscribed = False
            if racerunner.count() > 0:
                race.subscribed = True
    return render_to_response('team/index.html', 
    {
        'runner': runner,
        'future_races':  future_races,
        'race_maintypes': race_maintypes,
    }, 
    context_instance=RequestContext(request))  

# elenco atleti
def runners_list(request):
	runners_list = Runner.objects.all().order_by('name')
	return render_to_response('team/runner/index.html', 
	  {'runners_list': runners_list}, 
	  context_instance=RequestContext(request))

# dettaglio atleta    
def runner_details(request, runner_id):
	runner = get_object_or_404(Runner, pk=runner_id)
	racerunners = runner.racerunner_set.all().order_by('-race__date')
	race_maintypes = RaceType.objects.all().filter(is_maintype=True)
	return render_to_response('team/runner/details.html', 
	  {'runner': runner, 'racerunners': racerunners, 'race_maintypes': race_maintypes }, 
	  context_instance=RequestContext(request))
    
def future_races_list(request):
    user = request.user
    runner = None
    if user.is_anonymous() == False:
        runner = user.get_runner()
    return render_to_response('team/race/future_races.html', 
        {'runner': runner}, context_instance=RequestContext(request))
	
# dettaglio gara    
def race_details(request, race_id):
	race = get_object_or_404(Race, pk=race_id)
	racerunner = ""
	user = request.user
	runnerid = 0
	if user.is_anonymous() == False:
	  runnerid = user.get_runner().id
	racerunner = race.racerunner_set.filter(runner__id=runnerid)
	if race.is_future() == True:
	  racerunners = race.racerunner_set.all()
	  retires = None
	else:
	  racerunners = race.racerunner_set.filter(is_completed=True).order_by('ranking')
	  retires = race.racerunner_set.filter(is_completed=False)
	# Photos for this race
	pools = Pool.objects.filter(object_id=race_id) 
	return render_to_response('team/race/details.html', 
	  {'race': race, 'racerunners': racerunners, 'retires': retires, 'racerunner': racerunner, 'pools': pools}, 
	  context_instance=RequestContext(request))

# form di iscrizione  
class SubscriptionForm(forms.Form):
    subscribed = forms.BooleanField(required=False)

# iscrizione gara    
def race_subscribe(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    user = request.user
    runner = user.get_runner()
    racerunner = race.racerunner_set.filter(runner__id=runner.id)
    if racerunner.count() > 0:
        # rimuovo iscrizione
        racerunner.delete()
    else:
        # aggiungo iscrizione
        racerunner = RaceRunner(race=race,runner=runner)
        racerunner.save()
    return HttpResponseRedirect('/')

# modifica atleta   
def runner_update(request):
  user = request.user
  runner = user.get_runner()
  if request.method == 'POST':
    form = RunnerForm(request.POST, request.FILES, instance=runner)
    if form.is_valid():
      form.save()
    else:
      print 'errors to save'
  else:
    form = RunnerForm(instance=runner)
  return render_to_response("team/runner/update.html", 
    { "form": form, "runner": runner, },
    context_instance=RequestContext(request))

    
@login_required
def race_photo_add(request, race_id, template_name="team/race/add_photo.html"):
    race = get_object_or_404(Race, pk=race_id)
    
    form_class=PhotoUploadForm
    photo_form = form_class()
    if request.method == 'POST':
        if request.POST.get("action") == "upload":
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.member = request.user
                photo.save()
                
                # in group context we create a Pool object for it
                if race:
                    pool = Pool()
                    pool.photo = photo
                    # aggiunge gara al pool
                    race.associate(pool)
                    pool.save()
                
                request.user.message_set.create(message=_("Successfully uploaded photo '%s'") % photo.title)
                
                include_kwargs = {"id": photo.id}
                redirect_to = reverse("photo_details", kwargs=include_kwargs)
                
                return HttpResponseRedirect(redirect_to)

    return render_to_response(template_name, {
        "race": race,
        "photo_form": photo_form,
    }, context_instance=RequestContext(request))

#test   
def test(request):
	return render_to_response('test.html')
	
