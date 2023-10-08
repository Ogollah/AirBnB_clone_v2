#!/usr/bin/python3
# Full deployment of web static

from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['54.152.129.123', '35.175.135.158']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Compress directory to create an archive file.

    Returns:
        str: Path to the archive file on success; None on failure.
    """
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_' + now + '.tgz'

    # Create the archive
    local('mkdir -p versions/')
    result = local('tar -cvzf {} web_static/'.format(archive_path))

    # Check if archiving was successful
    return archive_path if result.succeeded else None


def do_deploy(archive_path):
    """Deploy web files to the server."""
    try:
        if not os.path.exists(archive_path):
            return False

        # Upload the archive
        put(archive_path, '/tmp/')

        # Create the target directory
        timestamp = archive_path[-18:-4]
        target_dir = '/data/web_static/releases/web_static_{}/'.format(
            timestamp)
        run('sudo mkdir -p {}'.format(target_dir))

        # Uncompress the archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C {}'.
            format(timestamp, target_dir))

        # Remove the archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Move contents into the host's web_static directory
        run('sudo mv {}/web_static/* {}'.format(target_dir, target_dir))

        # Remove the extraneous web_static directory
        run('sudo rm -rf {}/web_static'.format(target_dir))

        # Delete the pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish the symbolic link
        run('sudo ln -s {} /data/web_static/current'.format(target_dir))

    except Exception as e:
        return False

    return True


def deploy():
    """Deploy web static using do_pack and do_deploy."""
    return do_deploy(do_pack())
