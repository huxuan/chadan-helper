#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: test.py
Author: huxuan
Email: i(at)huxuan.org
Description: Chadan helper
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Timer
from urllib.parse import quote
import base64
import json
import random
import time

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from python_json_config import ConfigBuilder
import requests

CONFIG_FILENAME = 'config.json'

BASE_URL = 'http://api.chadan.cn'
CONFIRM_URL = '{}/order/confirmOrderdd623299'.format(BASE_URL)
LOGIN_URL = '{}/user/login'.format(BASE_URL)
ORDER_URL = '{}/order/getOrderdd623299'.format(BASE_URL)
PUBKEY_URL = '{}/user/getPublicKey'.format(BASE_URL)
SPECIAL_ORDER_URL = '{}/order/getSpecialOrder'.format(BASE_URL)

OPERATORS = {
    'MOBILE': '移动',
    'TELECOM': '电信',
    'UNICOM': '联通',
}
OPERATOR_SPECIAL = 'SPECIAL'

SC_URL = 'https://sc.ftqq.com/{}.send?text={}&desp={}'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PUBKEY_FORMAT = """-----BEGIN PUBLIC KEY-----
{}
-----END PUBLIC KEY-----"""
NOTIFICATION_KEY_FORMAT = '{} {}{} {}'
TITLE_GET_ORDER_FORMAT = '[CH]已抢单 {}元'
TITLE_CONFIRM_ORDER_FORMAT = '[CH]报单 {} {}'

TEXT_EXIT = 'Chadan-helper 将要退出啦'


class ChadanHelper():
    """Helper for chandan."""
    def __init__(self):
        super(ChadanHelper, self).__init__()
        self._parse_config()
        self.loop_status = True
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
        quote_password = quote(enc_password)

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
        executor = ThreadPoolExecutor(len(self.config.options))
        for option in self.config.options:
            future = executor.submit(self._get_order_wrapper, *option)
            future.add_done_callback(lambda x: x.result())
        try:
            while True:
                time.sleep(self.config.sleep_duration)
        except KeyboardInterrupt:
            print(TEXT_EXIT)
            self.loop_status = False
            executor.shutdown(wait=False)

    def _parse_config(self):
        """Parse configuration."""
        builder = ConfigBuilder()
        config = builder.parse_config(CONFIG_FILENAME)
        config.confirm_delay = config.confirm_delay or random.randint(500, 600)
        config.options = [option for option in config.options if option[1]]
        config.sleep_duration = config.sleep_duration or 0.5
        self.config = config

    def _get_order_wrapper(self, value, amount, operators):
        """Wrapper for get_order."""
        while self.loop_status and amount:
            for operator in operators:
                if self.loop_status and amount > 0:
                    res_json = self._get_order(value, amount, operator)
                    amount -= self._post_order(
                        res_json, value, amount, operator)

    def _get_order(self, value, amount, operator):
        """Get Order."""
        url = SPECIAL_ORDER_URL
        data = {
            'JSESSIONID': self.session_id,
            'faceValue': value,
            'amount': amount,
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
                return res.json()
            except json.JSONDecodeError:
                print(res.text)
        except requests.exceptions.RequestException as exc:
            print(exc)
        return {}

    def _post_order(self, res_json, value, amount, operator):
        """Post processing after getting order."""
        head = '{} {:>3} {:>2} {:>7}'.format(
            datetime.utcnow().strftime(DATETIME_FORMAT),
            value, amount, operator)
        msg = res_json.get('errorMsg', res_json)
        data = res_json.get('data', {})
        if msg == 'OK':
            print('{} 抢到 {} 单'.format(head, len(data)))
            for order in data:
                key = NOTIFICATION_KEY_FORMAT.format(
                    order['rechargeAccount'],
                    order['product']['province'],
                    OPERATORS[order['product']['operator']],
                    order['product']['faceValue'])
                if self.config.auto_confirmation:
                    Timer(self.config.confirm_delay, self._confirm_order,
                          [order['id'], key]).start()
                title = TITLE_GET_ORDER_FORMAT.format(key)
                self._send_sc_notification(title, json.dumps(order))
        else:
            print('{} {}'.format(head, msg))
        time.sleep(self.config.sleep_duration)
        return len(data)

    def _confirm_order(self, order_id, key):
        """Confirm order with some delay."""
        data = {
            'JSESSIONID': self.session_id,
            'id': order_id,
            'orderStatus': 1,
            'submitRemark': None,
        }
        res = self.session.post(CONFIRM_URL, data=data)
        title = TITLE_CONFIRM_ORDER_FORMAT.format(
            key, res.json()['errorMsg'][-5:])
        self._send_sc_notification(title, res.text)

    def _send_sc_notification(self, text, desp=''):
        """Send sc notification."""
        for sckey in self.config.sckeys:
            res = requests.get(SC_URL.format(sckey, quote(text), quote(desp)))
            print(res.json())
