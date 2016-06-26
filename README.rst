============
Najdi-si-sms
============



.. image:: https://travis-ci.org/brodul/najdi-si-sms.svg?branch=master
        :target: https://travis-ci.org/brodul/najdi-si-sms
        :alt: Master Travis CI Status

.. image:: https://readthedocs.org/projects/najdisi-sms/badge/?version=latest
        :target: http://najdisi-sms.readthedocs.io/en/latest/
        :alt: Latest Documentation Status

Command line utility to send automated sms through Slovenian Najdi.si service (40 sms per day for free).

For additional information visit `the documentation`_

.. _`the documentation`: http://najdisi-sms.readthedocs.io/en/latest/

How to use
==========


Installation
++++++++++++

From pypi
---------

You need the python-pip package and super user access to install system wide::

  pip install najdisi-sms

You can also install the package in virtualenv::

  virtualenv venv
  source venv/bin/activate
  pip install najdisi-sms

The CLI command can be found in "venv/bin/najdisi-sms" and you can add it to you PATH or call it directly.


From source
-----------

You can install the package systemwide with (you need su access)::

  make install
  #or
  pip install .

If you dont want/have super user access, you can install it in a python virtual env
in the root folder call::

  virtualenv venv
  source venv/bin/activate
  pip install .

The CLI command can be found in "venv/bin/najdisi-sms" and you can add it to you PATH or call it directly.

Standalone CLI command
++++++++++++++++++++++

::

  Usage: najdisi-sms -u username -p password  RECEIVER_NUM  MESSAGE

  Options:
    -h, --help            show this help message and exit
    -u USERNAME, --username=USERNAME
                          Username
    -p PASSWORD, --password=PASSWORD
                          Password
    -A USERAGENT, --useragent=USERAGENT
                          HTTP User Agent

Example::

  najdisi-sms -u brodul -p FUBAR_PASS 031123456 "Pikica, rad te mam. (sent from cronjob)"

Python API
++++++++++

Example::

  from najdisi_sms import SMSSender

  sms = SMSSender('username', 'password')
  sms.send(
      '031123456',
      'Pikica, rad te mam. (sent from cronjob)'
  )
