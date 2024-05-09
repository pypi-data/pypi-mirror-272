from dbbackup.settings import STORAGE_OPTIONS


def get_backup_location():
    return STORAGE_OPTIONS.get('location')
