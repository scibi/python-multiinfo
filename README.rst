===============================
Python MultiInfo API
===============================

.. image:: https://badge.fury.io/py/multiinfo.png
    :target: http://badge.fury.io/py/multiinfo
    
.. image:: https://travis-ci.org/scibi/python-multiinfo.png?branch=master
        :target: https://travis-ci.org/scibi/python-multiinfo

.. image:: https://pypip.in/d/multiinfo/badge.png
        :target: https://crate.io/packages/multiinfo?version=latest


Python library for sending and receiving SMS messages with MultiInfo service provided by Polkomtel

* Free software: MIT license
* Documentation: http://python-multiinfo.rtfd.org.

Usage
-----

You can receive SMS messages like that::

        from multiinfo import multiinfo

        mi = multiinfo.smsapi(username='someuser',
                password='somepassword',
                serviceid='1234',
                keyfile='/path/to/keyfile.pem',
                certfile='/path/to/certfile.pem')
        
        msg = mi.get_sms(timeout=30, manual_confirm=True)

        print "{}: {}".format(msg['sender'], msg['content'])
        
        mi.confirm_sms(msg['message_id'])



Supported operations
--------------------

* Receive single SMS message
* Confirm SMS message reception

Operations to be implemented
----------------------------

* Send single SMS message
* Send long single SMS message
* Send binary SMS message
* Get SMS message status
* Cancel SMS message
* Send multiple SMS messages
* Get multiple SMS messages status
* Prepare multiple SMS messages status report
* Fetch this report
