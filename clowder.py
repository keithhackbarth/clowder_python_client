#!/usr/bin/env python
# coding: utf-8
import datetime
from requests_futures.sessions import FuturesSession

ALLOWED_KEYS = ('url', 'value', 'status', 'frequency')

api_key = None

def _send(data):

    url = data.get('url', 'http://www.clowder.io/api')

    session = FuturesSession()

    if api_key is not None:
        data['api_key'] = api_key

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