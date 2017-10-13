# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured

from maintenance_mode import io, settings


def get_maintenance_mode():
    # If maintenance mode is defined in settings, it has priority.
    if settings.MAINTENANCE_MODE is not None:
        return settings.MAINTENANCE_MODE

    value = io.read_file(settings.MAINTENANCE_MODE_STATE_FILE_PATH, '0')

    if value not in ['0', '1']:
        raise ValueError('state file content value is not 0|1')

    value = bool(int(value))
    return value


def set_maintenance_mode(value):
    # If maintenance mode is defined in settings, it can't be changed.
    if settings.MAINTENANCE_MODE is not None:
        raise ImproperlyConfigured('Maintenance mode cannot be set dynamically if defined in settings.')

    if not isinstance(value, bool):
        raise TypeError('value argument type is not boolean')

    value = str(int(value))
    io.write_file(settings.MAINTENANCE_MODE_STATE_FILE_PATH, value)
