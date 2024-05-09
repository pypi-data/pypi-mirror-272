import os
from django.conf import settings
from ..base import CommandBasic
from .utils import get_backup_location


class Command(CommandBasic):
    def handle(self):
        location = get_backup_location()
        if location:
            os.makedirs(location)
        os.makedirs(settings.MEDIA_ROOT)
