# -*- coding: utf-8 -*-
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

        :param send_mock: A mock
        :type send_mock: mock.MagicMock
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


class TestValidateData(unittest.TestCase):

    def test_should_succeed_if_only_valid_keys_given(self):
        clowder._validate_data({
            'name': 'my-test',
            'url': clowder.CLOWDER_API_URL,
            'value': 123,
            'status': 1,
            'frequency': 1098123098
        })

    def test_should_raise_error_if_invalid_data_given(self):
        self.assertRaisesRegexp(
            ValueError,
            "Invalid data keys 'herp, derp'",
            clowder._validate_data,
            {'name': 'Hey', 'status': 1, 'herp': 123, 'derp': 456}
        )

    def test_should_raise_error_if_missing_keys(self):
        self.assertRaisesRegexp(
            ValueError,
            "Missing keys 'name'",
            clowder._validate_data,
            {'value': 1}
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
        clowder.fail({'name': 'Invalid stuff'})
        send.assert_called_once()
        self.assert_send_contains_data(send, 'name', 'Invalid stuff')

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
            {'name': 'Test', 'status': 'should fail'}
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


class TestDelete(BaseClowderTestCase):

    @mock.patch('clowder._send')
    def test_should_use_correct_delete_url(self, send):
        clowder.delete('test')
        send.assert_called_once()
        self.assert_send_contains_data(send, 'url', clowder.CLOWDER_DELETE_URL)


class TestSubmit(BaseClowderTestCase):

    def test_should_raise_error_if_alert_not_given(self):
        self.assertRaisesRegexp(
            ValueError,
            "Alert required",
            clowder.submit,
            name='Hello',
            value=123
        )

    def test_should_raise_error_if_value_not_given(self):
        self.assertRaisesRegexp(
            ValueError,
            "Value required",
            clowder.submit,
            name='Test',
            alert=lambda x: (x > 10)
        )

    @mock.patch('clowder.fail')
    def test_should_call_fail_if_predicate_returns_true(self, fail):
        clowder.submit(alert=lambda x: x > 10, value=15)
        fail.assert_called_once()

    @mock.patch('clowder.ok')
    def test_should_call_ok_if_predicate_returns_false(self, ok):
        clowder.submit(alert=lambda x: x > 10, value=10)
        ok.assert_called_once()


class TestSend(BaseClowderTestCase):

    def setUp(self):
        super(TestSend, self).setUp()
        self.fixture = {'name': 'hello', 'status': 1}

    @mock.patch('requests_futures.sessions.FuturesSession.post')
    def test_should_use_default_clowder_api_url(self, post):
        clowder._send(self.fixture)
        post.assert_called_once()
        args = post.call_args[0]
        url = args[0]
        self.assertEqual(url, clowder.CLOWDER_API_URL)

    @mock.patch('requests_futures.sessions.FuturesSession.post')
    def test_should_contain_provided_data(self, post):
        clowder._send(self.fixture)
        post.assert_called_once()
        kwargs = post.call_args[1]
        self.assertIn('data', kwargs)
        self.assertEqual(kwargs['data'], self.fixture)

    def test_should_raise_error_if_invalid_data_given(self):
        self.assertRaisesRegexp(
            ValueError,
            "Invalid data keys 'herp'",
            clowder._send,
            {'name': 'Test', 'herp': 123}
        )

    def test_should_raise_error_if_missing_keys(self):
        self.assertRaisesRegexp(
            ValueError,
            "Missing keys 'name'",
            clowder._send,
            {'value': 1}
        )

# clowder.ok({
#    'name': 'CPU Percent',
#    'value': psutil.cpu_percent(interval=1),
#    'frequency': datetime.timedelta(minutes=0.5)
# })

# clowder.ok({
#    'name': 'Memory Utilization',
#    'value': psutil.phymem_usage().percent
# })
