#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

from argparse import ArgumentParser
import sys
if sys.version_info < (3, 0):
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser
import os
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig()
log = logging.getLogger("najdisi_sms")
log.setLevel(logging.INFO)


class SettingParser(object):
    """docstring for SettingParser"""
    def __init__(self, args=None):
        self.args = args or sys.argv[1:]

        home = os.path.expanduser('~')
        self.default_config_path = os.path.join(
            home,
            '.config',
            'najdisi_sms.ini'
        )

        self.argparser = self.create_argparser()
        self.parser_space = self.argparser.parse_args(self.args)

        self.namespace = self.merge_settings(self.parser_space)
        self.check_password_username(self.namespace)

    def create_argparser(self):
        parser = ArgumentParser()
        parser.add_argument(
            "rec_num",
            metavar=u"RECEIVER_NUM",
            help="slovenian phone number starting with 0"
        )
        parser.add_argument(
            "message",
            metavar=u"MESSAGE",
            help="SMS message (less than 160 characters)"
        )
        parser.add_argument(
            "-c",
            "--configfile",
            dest="config",
            help=u"Config file",
            default=self.default_config_path
        )
        parser.add_argument(
            "-u",
            "--username",
            dest="username",
            help=u"Username"
        )
        parser.add_argument(
            "-p",
            "--password",
            dest="password",
            help=u"Password"
        )
        parser.add_argument(
            "-A",
            "--useragent",
            dest="useragent",
            help=u"HTTP User Agent",
            default="Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.2.3)"
            + "Gecko/20100401 Firefox/3.6.3"
        )
        return parser

    def merge_settings(self, parser_space):
        """
        Merge config file and cli options
        """

        def parse_ini(file_path):
            config = ConfigParser()
            config.read(file_path)
            return config

        if os.path.exists(parser_space.config):
            ini_config = parse_ini(parser_space.config)
            for attr in ['username', 'password']:
                setattr(
                    parser_space,
                    attr,
                    getattr(parser_space, attr, None) or ini_config.get('najdisi_sms', attr)
                )
        elif not self.default_config_path == parser_space.config:
            log.info('Config file you specified not found!')

        return parser_space

    def check_password_username(self, namespace):
        for attr in ['username', 'password']:
            if not getattr(namespace, attr):
                raise LookupError("Missing {}!".format(attr))


def main():
    parser = SettingParser()
    namespace = parser.namespace
    # parser = create_argparser()
    # namespace = parser.parse_args()
    #
    # namespace = merge_settings(parser, namespace)
    # try:
    #     check_password_username(namespace)
    # except LookupError as e:
    #     parser.print_help()
    #     log.error(e.args[0])
    #     parser.exit(1)

    sender = SMSSender(namespace.username, namespace.password, namespace.useragent)
    sender.send(namespace.rec_num, namespace.message)


class SMSSender(object):
    """Docstring for SMSSender. """

    def __init__(self, username, password, useragent=""):
        """@todo: to be defined1. """
        self.username = username
        self.password = password
        da = "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.2.3)" \
            + "Gecko/20100401 Firefox/3.6.3"
        self.useragent = useragent or da

    def normalize_receiver(self, receiver_num):
        """
        Split telephone number into area code and local number.


        :receiver_num: Telephone number string.
        :returns: Tuple with area code and local number.

        """
        # 031 123 456
        who = receiver_num.strip()

        # don't change
        # 031 123 456 => 123456
        recipent = who.replace(' ', '')[3:]
        # 031 123 456 =>  031
        base_code = who[:3]

        return base_code, recipent

    def check_msg_leng(self, msg):
        """
        Checks the message length raises an exception if more than 160 chars.

        :msg: Message
        :returns: Returns non modified msg

        """
        if len(msg) > 160:
            raise Exception('Message to long')

        return msg

    def send(self, receiver, msg):
        """send the message.

        :receiver: Receiver number (only Slovenian supported)
        :msg: SMS body message
        :returns: True if sending succeeded, else False.

        """

        msg = self.check_msg_leng(msg)

        base_code, recipient = self.normalize_receiver(receiver)

        log.info('Network code: %s', base_code)
        log.info('Receiver : %s', recipient)
        log.info('Message: %s', msg)
        log.info('Sending SMS ...')

        self.s = requests.Session()
        self.s.headers.update({'User-Agent': self.useragent})

        response = self.s.get(
            'http://www.najdi.si/najdi.layoutnajdi.loginlink:login?t:ac=sms'
        )

        soup = BeautifulSoup(response.text, "html.parser")
        formdata_els = soup.findAll(attrs={'name': 't:formdata'})
        formdata_value = formdata_els[0].attrs['value']

        data = {
            't:formdata': formdata_value,
            'jsecLogin': self.username,
            'jsecRememberMe': 'on',
            'jsecPassword': self.password
        }
        response = self.s.post(
            'http://www.najdi.si/prijava.jsecloginform',
            data
        )

        soup = BeautifulSoup(response.text)

        formdata_els = soup.findAll(attrs={'name': 't:formdata'})
        formdata_vals = [formdata_el.attrs['value'] for formdata_el in formdata_els]

        hidden_els = soup.findAll(attrs={'name': 'hidden'})
        hidden_value = hidden_els[0].attrs['value']

        data = {
            't:ac': 'sms',
            't:formdata': formdata_vals,
            'areaCodeRecipient': base_code,
            'phoneNumberRecipient': recipient,
            'selectLru': '',
            'hidden': hidden_value,
            'name': '',
            'text': msg,
            't:submit': '["send","send"]',
            't:zoneid': 'smsZone'
        }
        response = self.s.post(
            "http://www.najdi.si/najdi.shortcutplaceholder.freesmsshortcut.smsform",
            data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        soup = BeautifulSoup(response.text)

if __name__ == '__main__':
    main()
