#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/iot-seed/")
sys.path.insert(
    0, "/var/www/iot-seed/api/env/lib/python3.9/site-packages")

from api import create_app
application = create_app()

# deploying on apache
# user this as a minimal config
'''
<VirtualHost *:80>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        ServerName mdupuis.com
        WSGIDaemonProcess flaskapp user=pi group=gpio
        WSGIScriptAlias / /var/www/iot-seed/flaskapp.wsgi

        <Directory /var/www/iot-seed/api/>
                WSGIProcessGroup flaskapp
                WSGIApplicationGroup %{GLOBAL}
                WSGIScriptReloading On
                Order deny,allow
                Allow from all
        </Directory>
</VirtualHost>

'''
# make sure user 'pi' exists
# make sure group 'gpio' exists
