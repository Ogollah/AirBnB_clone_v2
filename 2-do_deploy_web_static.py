#!/usr/bin/python3
# Compress packages

from fabric.api import local, cd, put, run, env
from os import path
from datetime import datetime

env.hosts = ['54.152.129.123', '35.175.135.158']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Function to compress content

    Return: Archive path
    """
    # Time
    now = datetime.now()
    now = now.strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_' + now + '.tgz'

    # Archives
    local('mkdir -p versions/')
    result = local('tar -cvzf {} web_static/'.format(archive_path))

    # Check archiving
    if result.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    if not path.exists(archive_path):
        return False

    # Extract the timestamp from the archive path
    timestamp = archive_path[-18:-4]

    # Define target directory
    target_dir = '/data/web_static/releases/web_static_{}/'.format(timestamp)

    try:
        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')

        # Create the target directory
        run('sudo mkdir -p {}'.format(target_dir))

        # Uncompress the archive and delete it
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C {}'.
            format(timestamp, target_dir))

        # Remove the archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Move contents to the parent directory and delete the subdirectory
        run('sudo mv {}/web_static/* {}'.format(target_dir, target_dir))
        run('sudo rm -rf {}/web_static'.format(target_dir))

        # Update the symbolic link
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(target_dir))
    except Exception as e:
        return False

    return True
