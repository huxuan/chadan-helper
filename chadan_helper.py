#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: test.py
Author: huxuan
Email: i(at)huxuan.org
Description: Chadan helper
"""
from multiprocessing import Pool
import base64
import time
import urllib

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import requests

BASE_URL = 'http://api.chadan.cn'
LOGIN_URL = '{}/user/login'.format(BASE_URL)
ORDER_URL = '{}/order/getOrderdd623299'.format(BASE_URL)
PUBKEY_URL = '{}/user/getPublicKey'.format(BASE_URL)
SC_URL = 'https://sc.ftqq.com/{}.send?text={}&desp{}'

PUBKEY_FORMAT = """-----BEGIN PUBLIC KEY-----
{}
-----END PUBLIC KEY-----"""

TEXT_GET_ORDER = 'Chadan-helper 抢到单子啦'


class ChadanHelper():
    """Helper for chandan."""
    def __init__(self, config):
        super(ChadanHelper, self).__init__()
        self.config = config
        self.session = requests.Session()
        self.session_id = None

    def login(self):
        """Login."""
        # Encrypt password with public_key and random_str.
        data = {'userNo': self.config.username}
        res = self.session.post(PUBKEY_URL, data=data)
        print(res.json())
        public_key = PUBKEY_FORMAT.format(res.json()['data']['public_key'])
        random_str = res.json()['data']['random_str']
        key = RSA.importKey(public_key)
        rsa = PKCS1_v1_5.new(key)
        msg = (self.config.password + random_str).encode()
        enc_password = base64.b64encode(rsa.encrypt(msg))
        quote_password = urllib.parse.quote(enc_password)

        # Login with encrypted password.
        data = {
            'userNo': self.config.username,
            'loginPwd': quote_password,
        }
        res = self.session.post(LOGIN_URL, data=data)
        print(res.json())
        self.session_id = self.session.cookies.get_dict()['JSESSIONID']

    def get_orders(self):
        """Get Orders."""
        with Pool(self.config.pool_limit) as pool:
            for value, amount, operators in self.config.options:
                # self._get_order_wrapper(value, amount, operators)
                pool.apply_async(self._get_order_wrapper,
                                 (value, amount, operators))
            pool.close()
            pool.join()

    def _get_order_wrapper(self, value, amount, operators):
        """Wrapper for get_order."""
        res = None
        while amount:
            for operator in operators:
                res = self._get_order(value, operator, amount)
                if res is not None and res.get('data'):
                    self._send_sc_notification(TEXT_GET_ORDER)
                    amount -= len(res['data'])
                    break
                time.sleep(self.config.sleep_duration)

    def _get_order(self, value, operator, amount):
        """Get Order."""
        head = '{:>3} {:>7} {:>2}'.format(value, operator, amount)
        data = {
            'JSESSIONID': self.session_id,
            'faceValue': value,
            'province': None,
            'amount': amount,
            'operator': operator,
            'channel': 1,
        }
        try:
            res = self.session.post(ORDER_URL, data=data)
            if res.json().get('errorMsg'):
                if res.json()['errorMsg'] == 'OK':
                    print('{} 抢到 {} 单'.format(
                        head, len(res.json().get('data', []))))
                else:
                    print('{} {}'.format(head, res.json()['errorMsg']))
            else:
                print('{} {}'.format(head, res.json()))
            return res.json()
        except Exception as exc:
            print('{} {}'.format(head, exc))

    def _send_sc_notification(self, text, desp=None):
        """Send sc notificaiton."""
        for sckey in self.config.sckeys:
            requests.get(SC_URL.format(sckey, text, desp))
