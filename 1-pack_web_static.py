#!/usr/bin/python3
# Compress content before upload

from fabric.api import local
from datetime import datetime


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
