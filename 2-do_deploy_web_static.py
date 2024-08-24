#!/usr/bin/python3
"""
A function for deploying web_static content to web servers.
"""
from fabric.api import env, run, put
from datetime import datetime
import shlex
import os

env.hosts = ['54.89.58.11', '34.232.69.60']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """deploy"""
    if not os.path.exists(archive_path):
        return False
    try:
        filename = os.path.basename(archive_path)
        web_static_folder = filename.split('.')[0]
        # realese path and tmp path
        release_path = '/data/web_static/releases/{}'.format(web_static_folder)
        temp_path = '/tmp/{}'.format(filename)
        # put archive file into tmp folder
        put(archive_path, temp_path)
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf {} -C {}'.format(temp_path, release_path))
        # delet tmp folder
        run('rm -r {}'.format(temp_path))
        run('mv {}/web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))
        print('New version deployed!')
        return True
    except Exception as e:
        print('Error: {}'.format(e))
        return False
