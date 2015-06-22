# -*- coding: utf-8 -*-
import contextlib
import datetime
import unittest

import clowder
import mock

# import psutil


class BaseClowderTestCase(unittest.TestCase):
    """Base class for all clowder test cases."""

    def assert_send_contains_data(self, send_mock, key, value):
        """Assert that the given send mock was called with the given key and
        value pair.

        :param key: A key
        :type key: hashable
        :param value: The expected value
        :type value: mixed
        """
        self.assertIn(key, send_mock.call_args[0][0])
        self.assertEqual(value, send_mock.call_args[0][0][key])


class TestCleanFrequency(unittest.TestCase):

    def test_should_return_value_if_int_given(self):
        self.assertEqual(100, clowder._clean_frequency(100))

    def test_should_return_total_seconds_if_timedelta_given(self):
        fixture = datetime.timedelta(hours=1)
        self.assertEqual(
            fixture.total_seconds(), clowder._clean_frequency(fixture)
        )

    def test_should_raise_error_if_any_other_type_value_given(self):
        self.assertRaisesRegexp(
            ValueError,
            "Invalid frequency 'hello'",
            clowder._clean_frequency,
            "hello"
        )


class TestFail(BaseClowderTestCase):

    def test_should_raise_error_if_status_given(self):
        self.assertRaisesRegexp(
            AttributeError,
            "Status should not be provided to fail",
            clowder.fail,
            {'status': 'should fail'}
        )

    @mock.patch('clowder._send')
    def test_should_send_value_provided_along(self, send):
        clowder.fail({'value': 'Invalid stuff'})
        send.assert_called_once()
        self.assert_send_contains_data(send, 'value', 'Invalid stuff')

    @mock.patch('clowder._send')
    def test_should_send_status_of_negative_one(self, send):
        clowder.fail({'value': "Invalid stuff"})
        send.assert_called_once()
        self.assert_send_contains_data(send, 'status', -1)


class TestOk(BaseClowderTestCase):

    def test_should_raise_error_if_status_given(self):
        self.assertRaisesRegexp(
            AttributeError,
            "Status should not be provided to ok",
            clowder.ok,
            {'status': 'should fail'}
        )

    @mock.patch('clowder._send')
    def test_should_send_value_provided_along(self, send):
        clowder.ok({'value': 'Invalid stuff'})
        send.assert_called_once()
        self.assert_send_contains_data(send, 'value', 'Invalid stuff')

    @mock.patch('clowder._send')
    def test_should_send_status_of_one(self, send):
        clowder.ok({'value': "Invalid stuff"})
        send.assert_called_once()
        self.assert_send_contains_data(send, 'status', 1)

# clowder.ok({
#    'name': 'CPU Percent',
#    'value': psutil.cpu_percent(interval=1),
#    'frequency': datetime.timedelta(minutes=0.5)
# })

# clowder.ok({
#    'name': 'Memory Utilization',
#    'value': psutil.phymem_usage().percent
# })
