#!/usr/bin/python3
# eletes out-of-date archives, using the function do_clean

from fabric.api import env, run, local
from datetime import datetime
import os

env.hosts = ['54.152.129.123', '35.175.135.158']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
env.use_ssh_config = False


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): Number of archives to keep (including the most recent).
    """
    try:
        number = int(number)

        # Ensure that at least the most recent version is kept
        if number < 1:
            number = 1

        # List archives in the versions folder
        with cd('/data/web_static/releases'):
            archives = run('ls -t').split()

        # Delete unnecessary archives in /data/web_static/releases
        for archive in archives[number:]:
            run('rm -f {}'.format(archive))

        # List archives in the versions folder
        with cd('versions'):
            archives = local('ls -t', capture=True).split()

        # Delete unnecessary archives in the local 'versions' folder
        for archive in archives[number:]:
            local('rm -f {}'.format(archive))
    except Exception as e:
        pass


def clean_local():
    """
    Clean local 'versions' folder.
    """
    local('rm -f versions/*')
