#!/usr/bin/env python
# coding: utf-8
import datetime
from requests_futures.sessions import FuturesSession

ALLOWED_KEYS = ('url', 'value', 'status', 'frequency')

def _send(data):

    url = data.get('url', 'http://www.clowder.io/api')

    session = FuturesSession()

    if 'publisher' not in data:
        data['publisher'] = 1

    if 'value' not in data:
        data['value'] = data['status']

    if 'frequency' in data:
        data['frequency'] = _clean_frequency(data['frequency'])

    session.post(url, data=data)

def ok(data):

    if 'status' in data:
        raise AttributeError('Status should not be provided to okay')
    else:
        data['status'] = 1

    _send(data)

def fail(data):

    if 'status' in data:
        raise AttributeError('Status should not be provided to okay')
    else:
        data['status'] = -1

    _send(data)

def _clean_frequency(frequency):
    if isinstance(frequency, int):
        return frequency
    elif isinstance(frequency, datetime.timedelta):
        return int(frequency.total_seconds())

    raise ValueError('Invalid frequency')