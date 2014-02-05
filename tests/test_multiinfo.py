#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_multiinfo
----------------------------------

Tests for `multiinfo` module.
"""

import unittest
import httpretty
from sure import expect


from multiinfo import multiinfo


class TestMultiinfo(unittest.TestCase):

    def setUp(self):
        pass

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

        mi = multiinfo.smsapi(username='username',
                              password='password',
                              serviceid='1234',
                              keyfile='keyfile.pem',
                              certfile='certfile.pem')

        msg = mi.get_sms(timeout=30, manual_confirm=True)

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

        mi = multiinfo.smsapi(username='username',
                              password='password',
                              serviceid='1234',
                              keyfile='keyfile.pem',
                              certfile='certfile.pem')


        with self.assertRaises(multiinfo.NoNewSMS):
            msg = mi.get_sms(timeout=30, manual_confirm=True)

    @httpretty.activate
    def test_get_sms_error(self):
        httpretty.register_uri(httpretty.GET,
                               "https://api1.multiinfo.plus.pl/getsms.aspx",
                               body=("-24\nUsługa o podanym identyfikatorze "
                                     "nie jest aktywna"),
                               content_type="text/html")

        mi = multiinfo.smsapi(username='username',
                              password='password',
                              serviceid='1234',
                              keyfile='keyfile.pem',
                              certfile='certfile.pem')

        with self.assertRaises(multiinfo.StatusError):
            msg = mi.get_sms(timeout=30, manual_confirm=True)

    @httpretty.activate
    def test_confirm_sms_ok(self):
        httpretty.register_uri(httpretty.GET,
                               "https://api1.multiinfo.plus.pl/confirmsms.aspx",
                               body="0\r\nOK",
                               content_type="text/html")

        mi = multiinfo.smsapi(username='username',
                              password='password',
                              serviceid='1234',
                              keyfile='keyfile.pem',
                              certfile='certfile.pem')

        mi.confirm_sms(message_id='64031847')

        expect(httpretty.last_request()).to.have.property(
            "querystring").being.equal({
            'login': ['username'],
            'password': ['password'],
            'smsId': ['64031847'],
            'deleteContent': ['false'],
        })

    @httpretty.activate
    def test_confirm_sms_error(self):
        httpretty.register_uri(httpretty.GET,
                               "https://api1.multiinfo.plus.pl/confirmsms.aspx",
                               body=("-31\r\nNieprawidłowa wartość "
                                     "identyfikatora wiadomości potwierdzanej"),
                               content_type="text/html")

        mi = multiinfo.smsapi(username='username',
                              password='password',
                              serviceid='1234',
                              keyfile='keyfile.pem',
                              certfile='certfile.pem')

        with self.assertRaises(multiinfo.StatusError):
            mi.confirm_sms(message_id='64031847')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
