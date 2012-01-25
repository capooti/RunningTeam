Installation
============

To create a test installation of RunningTeam, create a virtualenv, activate it and 
install the needed django packages:

    $ virtualenv runningteam_env
    $ source runningteam_env/bin/activate
    $ pip install django
    $ pip install django-threadedcomments
    $ pip install django-photologue
    $ pip install django-tagging
    $ pip install django-avatar
    $ pip install django-pagination
    $ pip install django-uni-form
    
Download the source code, create your settings.py file copying the settings.py.tmpl,
change it accordingly to your settings.
Then sync the database and run the test server:

    $ ./manage syncdb
    $ ./manage runserver
    
Now open your browser, go to the admin interface and add some data:

    http://localhost:8000/admin/
    
Finally check the front end of the application:

    http://localhost:8000/team/
    
    
