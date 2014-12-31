# Copyright (c) 2013 theo crevon
#
# See the file LICENSE for copying permission.

import os

from fabric.api import *
from string import Template


@task
def localshop_install():
    """Installs localshop in preexisting virtualenv"""
    version = os.environ['LOCALSHOP_VERSION']
    local("pip install localshop=={0}".format(version))
    local("pip install MySQL-python")


@task
def localshop_init():
    config = get_config()

    create_configuration_file(config)

    local("localshop syncdb --noinput")  # Ensure db is created by localshop
    local("localshop migrate")
    create_user(config['username'], config['password'], config['email'])
    if config['access_key'] and config['secret_key']:
        load_credentials(config['access_key'], config['secret_key'])
    if config['cidr_value']:
        load_cidr(config['cidr_value'], config['cidr_label'], config['cidr_require_credentials'])

def get_config():
    config = {
        "username": "localshop",
        "password": "localshop",
        "email": "admin@localshop.example.org",
        "access_key": "",
        "secret_key": "",
        "cidr_value": "0.0.0.0/0",
        "cidr_require_credentials": "1",
        "cidr_label": "everyone",
        "database_engine": "django.db.backends.sqlite3",
        "database_name": "/home/localshop/.localshop/localshop.db",
        "database_user": "",
        "database_password": "",
        "database_host": "",
        "database_port": "",
        "timezone": "America/Montreal",
        "delete_files": "0",
        }

    for item in config:
        key = 'LOCALSHOP_' + item.upper()
        if key in os.environ:
            config[item] = os.environ[key]

    #Sanitize booleans
    config['cidr_require_credentials'] = config['cidr_require_credentials'] == '1'
    config['delete_files'] = config['delete_files'] == '1'

    return config

def create_configuration_file(config):
    with open('localshop.conf.tpl') as template_file:
        template = Template(template_file.read())
        json_string = template.substitute(config)

        with open('/home/localshop/.localshop/localshop.conf.py', 'w') as json_file:
            json_file.write(json_string)


def load_credentials(access_key=None, secret_key=None):
    with open('credentials.json.tpl') as template_file:
        template = Template(template_file.read())
        json_string = template.substitute({'access_key': access_key, 'secret_key': secret_key})

        with open('credentials.json', 'w') as json_file:
            json_file.write(json_string)

    local("localshop loaddata credentials.json")

def load_cidr(cidr, label, require_credentials):
    with open('cidr.json.tpl') as template_file:
        template = Template(template_file.read())
        json_string = template.substitute({'require_credentials': 'true' if require_credentials else 'false',
                                           'cidr': cidr,
                                           'label': label})

        with open('cidr.json', 'w') as json_file:
            json_file.write(json_string)

    local("localshop loaddata cidr.json")

def create_user(user, password, email):
    user_command = """
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

try:
    User.objects.get_by_natural_key('{user}')
except ObjectDoesNotExist:
    User.objects.create_superuser('{user}', '{mail}', '{password}')
""".format(user=user, password=password, mail=email)

    local('echo "{inst}" | localshop shell'.format(inst=user_command))


