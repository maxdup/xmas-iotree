#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/xmas-iotree/")
sys.path.insert(0, "/var/www/xmas-iotree/api/env/lib/python3.9/site-packages")

from api import create_app
application = create_app('config')

# deploying on apache
# use this as a minimal config

# sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
# sudo a2enmod wsgi

'''
<VirtualHost *:80>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        ServerName iotproject.com
        WSGIDaemonProcess flaskapp user=pi group=gpio
        WSGIScriptAlias / /var/www/xmas-iotree/flaskapp.wsgi

        <Directory /var/www/xmas-iotree/api/>
                WSGIProcessGroup flaskapp
                WSGIApplicationGroup %{GLOBAL}
                WSGIScriptReloading On
                Order deny,allow
                Require all granted
        </Directory>
</VirtualHost>
'''
# make sure user 'pi' exists
# make sure group 'gpio' exists

# add /dev/mem permission
# usermod -a -G gpio pi

# sudo chown -R pi:pi /var/www


# sudo apt-get install rabbitmq-server
# sudo systemctl start rabbitmq-server
# sudo systemctl enable rabbitmq-server
