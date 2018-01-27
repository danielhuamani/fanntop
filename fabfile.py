from os.path import abspath, dirname, join
import sys
from fabric.colors import blue, green
from fabric.api import sudo, run, env, cd, local, settings, prefix, task
import json


@task
def run_local(ip=''):
    print(ip, "-------------")
    run = ('./src/manage.py runserver {0} --settings=config.settings.local').format(ip)
    local(run)

@task
def migrations(config):
    if not config:
        config = 'local'
    run = ('./src/manage.py makemigrations --settings=config.settings.{0}').format(config)
    local(run)

@task
def migrate(config):
    if not config:
        config = 'local'
    run = ('./src/manage.py migrate --settings=config.settings.{0}').format(config)
    local(run)

@task
def create_admin(config):
    run = ('./src/manage.py createsuperuser --settings=config.settings.{0}').format(config)
    local(run)
