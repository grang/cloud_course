#-*- coding: utf-8 -*-
from fabric.api import *

env.hosts = ['root@106.52.92.203']
env.passwords = {
    'root@106.52.92.203:22': 'OvD3tSWp'
}

env.roledefs = {
    'main': ['root@106.52.92.203:22']
}

REMOTE_DIR = '/root/yuwen_server'

@roles('main')
def migrate():
    with cd(REMOTE_DIR):
        run('git pull')
        run('python3 manage.py makemigrations')
        run('python3 manage.py migrate')

@roles('main')
def restart_server():
    with cd(REMOTE_DIR):
        run('git pull')
        run('supervisorctl restart yuwen')