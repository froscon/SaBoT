This software is currently developed and tested with django version 1.10.

The system is currently used with mod_wsgi in an apache environment. However, it is also
possible to use fastcgi. An example of a working apache config for mod_wsgi looks like:

	Alias /static/ 	/var/www/sabot/django/static/
	Alias /media	/var/www/sabot/django/media

	<Directory /var/www/sabot/django/static>
		Order deny,allow
		Allow from all
	</Directory>
	<Directory /var/www/sabot/django/media>
		Order deny,allow
		Allow from all
		Options -Indexes
	</Directory>
	<Directory /var/www/sabot/django/media/invoice_pdfs>
		Order deny,allow
		Deny from all
	</Directory>

	WSGIDaemonProcess sabot user=sabot group=sabot python-path=/var/www/sabot/django processes=2 threads=15 display-name=%{GROUP}
	WSGIProcessGroup sabot

	WSGIScriptAlias /	/var/www/sabot/django/sabot/wsgi.py

	<Directory /var/www/sabot/django/sabot>
		<Files wsgi.py>
			Order allow,deny
			allow from all
		</Files>
	</Directory>

In order to test the software, you may simply (as usual for django projects)
use "./manage.py runserver"

Before you start
- run "sudo pip install -r requirements.txt"
- create the following config files: 
	- sabot/settings.py
	- sabot/conferenceSettings.py
	- sabot/localSettings.py (and sabot/prodSettings.py if you want to distinguish a development and a production version) from their example files (prodSettings.py needs the same parameters)
- run "./manage.py migrate" to setup your database
- run "./manage.py createsuperuser" to create your admin account

If you want to use the invoice creation functionality, it is required that
you have libreoffice (or openoffice) installed on the server.

Here is a pretty good tutorial to run django apps with guniocorn behind an apache webserver: https://wiki.uberspace.de/cool:django (easy to adopt for SaBoT)
