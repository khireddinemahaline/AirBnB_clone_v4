#!/usr/bin/python3
"""Fabric script generates .tgz archive of all in web_static"""
from fabric.api import local, task, run, put, env
from datetime import datetime
import os

env.hosts = ['54.89.58.11', '34.232.69.60']
env.user = 'ubuntu'


@task
def deploy():
    """ DEPLOYS """
    try:
        archive_path = do_pack()
    except Exception as e:
        return False

    return do_deploy(archive_path)


def do_pack():
    """generate .tgz archive in der with name 'versions' """
    timenow = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timenow)
        local("tar -cvzf {} web_static/".format(filename))
        return filename
    except Exception as e:
        return None


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
