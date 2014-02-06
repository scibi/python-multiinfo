#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_multiinfo
----------------------------------

Tests for `multiinfo` module.
"""

import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

import httpretty
from sure import expect
import re


from multiinfo import multiinfo


class TestMultiinfo(unittest.TestCase):

    def setUp(self):
        self.mi = multiinfo.smsapi(username='username',
                                   password='password',
                                   serviceid='1234',
                                   keyfile='keyfile.pem',
                                   certfile='certfile.pem')

    @httpretty.activate
    def test_get_sms_text(self):
        httpretty.register_uri(httpretty.GET,
                               "https://api1.multiinfo.plus.pl/getsms.aspx",
                               body="""0
64031847
48692111111
48661222222
1
Test+1
0
0
1234
661333333
050214174507""",
                               content_type="text/html")

        msg = self.mi.get_sms(timeout=30, manual_confirm=True)

        expect(httpretty.last_request()).to.have.property(
            "querystring").being.equal({
            'login': ['username'],
            'password': ['password'],
            'serviceId': ['1234'],
            'timeout': ['30000'],
            'manualconfirm': ['true'],
            'deleteContent': ['false'],
        })

        from datetime import datetime
        expect(msg).being.equal({
            'status': 'ok',
            'message_id': '64031847',
            'sender': '48692111111',
            'receiver': '48661222222',
            'content_type': 'text',
            'raw_content': 'Test+1',
            'protocol_id': '0',
            'encoding_schema': '0',
            'service_id': '1234',
            'connector_id': '661333333',
            'raw_reveive_date': '050214174507',
            'reveive_date': datetime(year=2014, month=2, day=5, hour=17,
                                     minute=45, second=7),
            'content': 'Test 1',
        })

    @httpretty.activate
    def test_get_sms_nomsg(self):
        httpretty.register_uri(httpretty.GET,
                               "https://api1.multiinfo.plus.pl/getsms.aspx",
                               body="0\n-1",
                               content_type="text/html")

        self.assertRaises(multiinfo.NoNewSMS, self.mi.get_sms, timeout=30,
                          manual_confirm=True)

    @httpretty.activate
    def test_confirm_sms_ok(self):
        httpretty.register_uri(httpretty.GET,
                               ("https://api1.multiinfo.plus.pl"
                                   "/confirmsms.aspx"),
                               body="0\r\nOK",
                               content_type="text/html")

        self.mi.confirm_sms(message_id='64031847')

        expect(httpretty.last_request()).to.have.property(
            "querystring").being.equal({
            'login': ['username'],
            'password': ['password'],
            'smsId': ['64031847'],
            'deleteContent': ['false'],
        })

    def tearDown(self):
        pass


class TestMultiinfoError(unittest.TestCase):

    def setUp(self):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET,
                               re.compile('api1.multiinfo.plus.pl/(\w+).aspx'),
                               body=("-31\r\nNieprawidłowa wartość "
                                     "identyfikatora wiadomości "
                                     "potwierdzanej"),
                               content_type="text/html; charset=utf-8")

        self.mi = multiinfo.smsapi(username='username',
                                   password='password',
                                   serviceid='1234',
                                   keyfile='keyfile.pem',
                                   certfile='certfile.pem')

        self.msg_regexp = '^Wrong status.*Status: -31.*'\
            'Message: Nieprawidłowa wartość'

    def test_confirm_sms_error(self):
        self.assertRaisesRegexp(multiinfo.StatusError, self.msg_regexp,
                                self.mi.confirm_sms, message_id='64031847')

    def test_get_sms_error(self):
        self.assertRaisesRegexp(multiinfo.StatusError, self.msg_regexp,
                                self.mi.get_sms, timeout=30,
                                manual_confirm=True)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

if __name__ == '__main__':
    unittest.main()
