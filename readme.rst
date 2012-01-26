===========
RunningTeam
===========

A web application for managing a running team.

You can visit a RunningTeam powered web site (in Italian) `here
<http://capooti.webfactional.com/>`_. 

Prerequisites
=============

This django packages are mandatory:

* django-avatar
* django-pagination
* django-photologue
* django-tagging
* django-threadedcomments
* django-uni-form

Installation
============

To create a test installation of RunningTeam, create a virtualenv, activate it 
and install the needed django packages::

    $ mkdir runningteam
    $ virtualenv runningteam_env
    $ source runningteam_env/bin/activate
    $ pip install django
    $ pip install django-threadedcomments
    $ pip install django-photologue
    $ pip install django-tagging
    $ pip install django-avatar
    $ pip install django-pagination
    $ pip install django-uni-form
    
Download the source code, create your settings.py file copying the 
settings.py.tmpl, change it accordingly to your settings.
Then sync the database and run the test server::

    $ git clone git@github.com:capooti/RunningTeam.git
    $ cd RunningTeam/runningteam_env
    $ cp settings.py.tmpl settings.py
    $ vi settings.py
    $ ./manage syncdb
    $ ./manage runserver
    
Now open your browser, go to the admin interface and add some data:

    http://localhost:8000/admin/
    
Finally check the front end of the application:

    http://localhost:8000/team/
    
Credits
=======

RunningTeam uses extensively awesome Django packages developed by the Django 
Community (looks in prerequisites).

The internal groups, photos and threadedcomments_extra applications and some of
the css files are derived, with very small modifications, from the Pinax Project
(early versions of RunningTeam were running on the Pinax platform).

