import os
from dbbackup.settings import STORAGE_OPTIONS
from django.conf import settings
from ..base import CommandBasic


class Command(CommandBasic):
    def handle(self):
        location = STORAGE_OPTIONS.get('location')
        if location:
            os.makedirs(location)
        os.makedirs(settings.MEDIA_ROOT)
