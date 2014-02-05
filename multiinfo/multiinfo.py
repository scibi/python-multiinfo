#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

class NoNewSMS(Exception):
    """Raised by smsapi.getSMS when there is no new SMS."""
    pass

class StatusError(Exception):
    """Raised when API call returns status other than OK."""
    def __init__(self, status, message):
        self.status=status
        self.message=message
    def __str__(self):
        return "Wrong status exception. Status: {s.status} Message: {s.message}".format(s=self)



class smsapi:
    base_url = 'https://api1.multiinfo.plus.pl'
    path_get = '/getsms.aspx'
    path_confirm = '/confirmsms.aspx'

    def __init__(self, username, password, serviceid, keyfile, certfile):
        self.username = username
        self.password = password
        self.serviceid = serviceid
        self.cert = (certfile, keyfile)

    def get_sms(self, timeout=30, manual_confirm=False, delete_content=False):
        payload = {
            'login': self.username,
            'password': self.password,
            'serviceId': self.serviceid,
            'timeout': timeout*1000,
            'manualconfirm': ('false', 'true')[manual_confirm],
            'deleteContent': ('false', 'true')[delete_content],
        }
        r = requests.get(self.base_url+self.path_get, params=payload,
                         timeout=timeout+5, cert=self.cert)

        params = ['status', 'message_id', 'sender', 'receiver', 'content_type',
                  'raw_content', 'protocol_id', 'encoding_schema',
                  'service_id', 'connector_id', 'raw_reveive_date']

        lines = r.text.split('\n')
        msg = {}
        for i in range(len(lines)):
            msg[params[i]] = lines[i]

        if msg['status'] == '0':
            msg['status'] = 'ok'
        elif int(msg['status']) < 0:
            raise StatusError(lines[0],lines[1])

        if msg['message_id'] == '-1':
            raise NoNewSMS()

        if msg['content_type'] == '1':
            msg['content_type'] = 'text'
            import urllib
            msg['content'] = urllib.unquote_plus(msg['raw_content'])
        elif msg['content_type'] == '2':
            msg['content_type'] = 'binary'

        from datetime import datetime
        msg['reveive_date'] = datetime.strptime(msg['raw_reveive_date'],
                                                '%d%m%y%H%M%S')

        return msg
    def confirm_sms(self, message_id, delete_content=False):
        payload = {
            'login': self.username,
            'password': self.password,
            'smsId': message_id,
            'deleteContent': ('false', 'true')[delete_content],
        }
        r = requests.get(self.base_url+self.path_confirm, params=payload,
                         cert=self.cert)
        lines = r.text.split('\n')
        from pprint import pprint
        pprint(lines)
        pprint(r.headers)
        code=int(lines[0])
        if code!=0:
            raise StatusError(code,lines[1])
            


