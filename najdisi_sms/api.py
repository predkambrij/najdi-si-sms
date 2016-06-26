import requests
from bs4 import BeautifulSoup

from . import log


class SMSSender(object):
    """Docstring for SMSSender. """

    def __init__(self, username, password, useragent=""):
        """@todo: to be defined1. """
        self.username = username
        self.password = password
        da = "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.2.3)" \
            + "Gecko/20100401 Firefox/3.6.3"
        self.useragent = useragent or da
        self.s = requests.Session()

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
        formdata_vals = [formdata_el.attrs['value'] for
                         formdata_el in formdata_els]

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
            "http://www.najdi.si/"
            "najdi.shortcutplaceholder.freesmsshortcut.smsform",
            data,
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        soup = BeautifulSoup(response.text)
