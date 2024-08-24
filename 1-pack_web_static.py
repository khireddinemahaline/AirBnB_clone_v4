#!/usr/bin/python3
"""Fabric script generates .tgz archive of all in web_static"""
from fabric.api import local, task
from datetime import datetime


@task
def do_pack():
    """generate .tgz archive file with name 'versions' """
    timenow = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timenow)
        local("tar -cvzf {} web_static/".format(filename))
        return filename
    except Exception as e:
        return None
