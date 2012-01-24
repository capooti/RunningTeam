from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        # commento su gara
        notification.create_notice_type("race_comment", _("New comment for race"), _("A new comment has been inserted for a race"), default=2)
        # commento su gara
        notification.create_notice_type("photo_comment", _("New comment for photo"), _("A new comment has been inserted for a photo"), default=2)
        # nuova foto
        notification.create_notice_type("photo_new", _("New photo for race"), _("A new photo has been uploaded for a race"), default=2)

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
