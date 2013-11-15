from datetime import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms 
from django.forms.extras import widgets 
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

##########
# Models #
##########

class Runner(models.Model):
    """
    Model for Runner.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(_('name'), max_length=255)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField(_('birth date'), blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=10, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    certificate = models.FileField(_('certificate'), upload_to='certificates',
        blank=True, null=True)
    user = models.ForeignKey(User, unique=True, blank=True, null=True)

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('runner')
        verbose_name_plural = _('runners')

class RaceType(models.Model):
    """
    Model for RaceType.
    """
    name = models.CharField(_('name'), max_length=255)
    is_maintype = models.BooleanField(_('is maintype'))

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('race type')
        verbose_name_plural = _('race types')

class Race(models.Model):
    """
    Model for Race.
    """
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(verify_exists=False, blank=True, null=True)
    date = models.DateField(_('date'), blank=True, null=True)
    location = models.CharField(_('location'), max_length=255, 
        blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    racetype = models.ForeignKey(RaceType)

    def __unicode__(self):
        return '%s' % (self.name + ' (' + self.racetype.name + ')')
        
    def slug(self):
        return self.name.replace(' ','_')

    def is_future(self):
        if self.date>date.today():
          return True
        else:
          return False
          
    def associate(self, instance, commit=True):
        instance.object_id = self.id
        instance.content_type = ContentType.objects.get_for_model(self)
        if commit:
            instance.save()
        return instance
        
    class Meta:
        ordering = ['-date']
        verbose_name = _('race')
        verbose_name_plural = _('races')

class RaceRunner(models.Model):
    """
    Model for RaceRunner.
    """
    race = models.ForeignKey(Race)
    runner = models.ForeignKey(Runner)
    is_completed = models.BooleanField(_('is completed'), )
    ranking = models.PositiveSmallIntegerField(_('ranking'), null=True,
        blank=True)
    time = models.TimeField(_('time'), null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.race.name + ' - ' + self.runner.name)

##########
# Forms  #
##########

# form informazioni atleta
class RunnerForm(ModelForm):
    """
    Form for a Runner.
    """
    birhtdate = forms.DateField(label=_('birth date'),
        widget=widgets.SelectDateWidget(years=range(1900,2010))) 
        
    class Meta:
        model = Runner
        fields = ('name', 'nickname', 'gender', 'birhtdate', 'phone', 
            'certificate' )


##########
# Others #
##########

def get_racerunners_list(race):
    """
    Get a runners list for a given race.
    """
    races = gara.garaatleta_set.all()
    users = []
    for race in races:
        utenti.append(race.runner.user)
    return users

from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    """
    Manages a new comment.
    """
    # race comment
    if isinstance(instance.content_object, Race):
        race = instance.content_object
        if notification:
            users = get_racerunners_list(race)
            notification.send(users, "race_comment", 
                {"user": instance.user, "race": race, "comment": instance})
    # image comment
    if isinstance(instance.content_object, Image):
        pool = instance.content_object.pool_set.all()[0]
        race = pool.content_object
        if notification:
            users = get_racerunners_list(race)
            notification.send(users, "photo_comment", 
                {"user": instance.user, "race": race, 
                "comment": instance, "photo": pool.photo})
models.signals.post_save.connect(new_comment, sender=ThreadedComment)

from photos.models import Pool, Image
def new_photo(sender, instance, **kwargs):
    """
    Manages a new photo.
    """
    race = instance.content_object
    if notification:
        users = get_racerunners_list(race)
        notification.send(users, "photo_new", 
            {"user": instance.photo.member, "photo": instance.photo, 
                "race": race})
models.signals.post_save.connect(new_photo, sender=Pool)


