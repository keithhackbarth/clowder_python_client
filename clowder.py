#!/usr/bin/env python
# coding: utf-8
import datetime

from requests_futures.sessions import FuturesSession


# The URL of the Clowder API
CLOWDER_API_URL = 'http://www.clowder.io/api'
# Allowed keys for data given
ALLOWED_KEYS = ('url', 'value', 'status', 'frequency')

api_key = None


def _send(data):
    """Send data to the Clowder API.

    :param data: Dictionary of API data
    :type data: dict
    """
    url = data.get('url', CLOWDER_API_URL)

    session = FuturesSession()

    if api_key is not None:
        data['api_key'] = api_key

    if 'value' not in data:
        data['value'] = data['status']

    if 'frequency' in data:
        data['frequency'] = _clean_frequency(data['frequency'])

    session.post(url, data=data)


def ok(data):
    """Send a success signal to clowder.

    :param data: Data to be sent along (Should not include 'status')
    :type data: dict
    """
    if 'status' in data:
        raise AttributeError('Status should not be provided to okay')
    else:
        data['status'] = 1

    _send(data)


def fail(data):
    """Send a failure signal to clowder.

    :param data: Data to be sent along (Should not include 'status')
    :type data: dict
    """
    if 'status' in data:
        raise AttributeError('Status should not be provided to fail')
    else:
        data['status'] = -1

    _send(data)


def _clean_frequency(frequency):
    """Converts a frequency value to an integer. Raises an error if an invalid
    type is given.

    :param frequency: A frequency
    :type frequency: int or datetime.timedelta
    :rtype: int
    """
    if isinstance(frequency, int):
        return frequency
    elif isinstance(frequency, datetime.timedelta):
        return int(frequency.total_seconds())

    raise ValueError('Invalid frequency {!r}'.format(frequency))
