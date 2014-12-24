# Copyright (c) 2013 theo crevon
#
# See the file LICENSE for copying permission.

import os
import ConfigParser

from fabric.context_managers import prefix
from fabric.api import *


activate_virtualenv = "/bin/bash -c 'source /home/localshop/venv/bin/activate'"


@task
def localshop_install():
    """Installs localshop in preexisting virtualenv"""
    with prefix(activate_virtualenv):
        local("pip install localshop")
        local("pip install MySQL-python")


@task
def localshop_init():
    """Emulates the localshop init phase"""
    # Extract the user, pass and mail from config file,
    # assuming docker build has set them already
    config = ConfigParser.ConfigParser()
    config.read("localshop.conf")

    localshop_user = config.get('superuser', 'username')
    localshop_pass = config.get('superuser', 'password')
    localshop_mail = config.get('superuser', 'mail')

    # Compute localshop super creation instruction
    # from environement variables
    superuser_create = ensure_user_command(localshop_user, localshop_pass, localshop_mail)

    with prefix(activate_virtualenv):
        local("su localshop -c 'localshop syncdb --noinput'")  # Ensure db is created by localshop
        local("localshop migrate")
        local('echo "{inst}" | localshop shell'.format(inst=superuser_create))


def ensure_user_command(user, password, mail):
    return """
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

try:
    User.objects.get_by_natural_key('{user}')
except ObjectDoesNotExist:
    User.objects.create_superuser('{user}', '{mail}', '{password}')
""".format(user=user, password=password, mail=mail)


