#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: test.py
Author: huxuan
Email: i(at)huxuan.org
Description: Chadan helper
"""
try:
    import simplejson as json
except ImportError:
    import json

from datetime import datetime
from threading import Timer
from urllib.parse import quote
import base64
import random

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import requests

from notification import Notification

BASE_URL = 'http://api.chadan.cn'
CONFIRM_URL = '{}/order/confirmOrderdd623299'.format(BASE_URL)
LOGIN_URL = '{}/user/login'.format(BASE_URL)
ORDER_URL = '{}/order/getOrderdd623299'.format(BASE_URL)
PUBKEY_URL = '{}/user/getPublicKey'.format(BASE_URL)
SPECIAL_ORDER_URL = '{}/order/getSpecialOrder'.format(BASE_URL)

MAX_AMOUNT = [1, 1, 1, 4, 7, 10, 15]
OPERATORS = {
    'MOBILE': '移动',
    'TELECOM': '电信',
    'UNICOM': '联通',
}
OPERATOR_SPECIAL = 'SPECIAL'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
HEAD_FORMAT = '{} {:10} {} {:>3} {:>2} {:7}'
PUBKEY_FORMAT = """-----BEGIN PUBLIC KEY-----
{}
-----END PUBLIC KEY-----"""


class ChadanHelper():
    """Helper for chandan."""
    def __init__(self, config):
        super(ChadanHelper, self).__init__()
        self.config = config
        self.config.confirm_delay = self.config.confirm_delay or \
            random.randint(500, 600)
        self.max_amount = 1
        self.session = requests.Session()
        self.session_id = self._login()

    def _login(self):
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
        quote_password = quote(enc_password)

        # Login with encrypted password.
        data = {
            'userNo': self.config.username,
            'loginPwd': quote_password,
        }
        res = self.session.post(LOGIN_URL, data=data)
        print(res.json())
        self.max_amount = MAX_AMOUNT[res.json()['data']['userLevel'] - 1]
        return self.session.cookies.get_dict()['JSESSIONID']

    def get_order(self, value, amount, operator):
        """Get Order."""
        url = SPECIAL_ORDER_URL
        data = {
            'JSESSIONID': self.session_id,
            'faceValue': value,
            'amount': min(amount, self.max_amount),
            'channel': 1,
        }
        if operator != OPERATOR_SPECIAL:
            url = ORDER_URL
            data.update({
                'province': None,
                "operator": operator,
            })
        try:
            res = self.session.post(url, data=data)
            try:
                return self._post_order(res.json(), value, amount, operator)
            except json.JSONDecodeError:
                print(res.text)
        except requests.exceptions.RequestException as exc:
            print(exc)
        return 0

    def _post_order(self, res_json, value, amount, operator):
        """Post processing after getting order."""
        head = HEAD_FORMAT.format(
            datetime.utcnow().strftime(DATETIME_FORMAT),
            self.config.platform, self.config.username,
            value, amount, operator)
        msg = res_json.get('errorMsg', res_json)
        data = res_json.get('data', {})
        if msg == 'OK':
            print('{} 抢到 {} 单'.format(head, len(data)))
            for order in data:
                args = {
                    'platform': self.config.platform,
                    'username': self.config.username,
                    'mobile': order['rechargeAccount'],
                    'operator':
                        order['product']['province'] +
                        OPERATORS[order['product']['operator']],
                    'value': order['product']['faceValue']
                }
                if self.config.auto_confirmation:
                    Timer(self.config.confirm_delay, self._confirm_order,
                          [order['id'], args]).start()
                Notification.send_get_order(args)
        else:
            print('{} {}'.format(head, msg))
        return len(data)

    def _confirm_order(self, order_id, args):
        """Confirm order with some delay."""
        data = {
            'JSESSIONID': self.session_id,
            'id': order_id,
            'orderStatus': 1,
            'submitRemark': None,
        }
        res = self.session.post(CONFIRM_URL, data=data)
        args['msg'] = res.json()['errorMsg']
        Notification.send_confirm_order(args)
