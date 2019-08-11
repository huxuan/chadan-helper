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
SC_URL = 'https://sc.ftqq.com/{}.send?text={}&desp={}'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PUBKEY_FORMAT = """-----BEGIN PUBLIC KEY-----
{}
-----END PUBLIC KEY-----"""

TEXT_CONFIRM_FAIL = 'Chadan-helper 报单失败啦'
TEXT_CONFIRM_SUCCEED = 'Chadan-helper 报单成功啦'
TEXT_GET_ORDER = 'Chadan-helper 抢到单子啦'
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
        config.sleep_duration = config.sleep_duration or 1
        self.config = config

    def _get_order_wrapper(self, value, amount, operators):
        """Wrapper for get_order."""
        while self.loop_status and amount:
            for operator in operators:
                if self.loop_status and amount > 0:
                    res_json = self._get_order(value, amount, operator)
                    msg = res_json.get('errorMsg', res_json)
                    head = '{} {:>3} {:>2} {:>7}'.format(
                        datetime.utcnow().strftime(DATETIME_FORMAT),
                        value, amount, operator)
                    if msg == 'OK':
                        data = res_json.get('data', [])
                        amount -= len(data)
                        if data:
                            self._post_order(data)
                        print('{} 抢到 {} 单'.format(head, len(data)))
                    else:
                        print('{} {}'.format(head, msg))
                    time.sleep(self.config.sleep_duration)

    def _get_order(self, value, amount, operator):
        """Get Order."""
        data = {
            'JSESSIONID': self.session_id,
            'faceValue': value,
            'province': None,
            'amount': amount,
            "operator": operator,
            'channel': 1,
        }
        try:
            res = self.session.post(ORDER_URL, data=data)
            return res.json()
        except requests.exceptions.RequestException as exc:
            print(exc)
        return {}

    def _post_order(self, data):
        """Post processing after getting order."""
        if self.config.auto_confirmation:
            for order in data:
                Timer(self.config.confirm_delay,
                      self._confirm_order, [order['id']]).start()
        self._send_sc_notification(TEXT_GET_ORDER, json.dumps(data))

    def _confirm_order(self, order_id):
        """Confirm order with some delay."""
        data = {
            'JSESSIONID': self.session_id,
            'id': order_id,
            'orderStatus': 1,
            'submitRemark': None,
        }
        res = self.session.post(CONFIRM_URL, data=data)
        if res.status_code != 200:
            self._send_sc_notification(TEXT_CONFIRM_FAIL, res.text)
        else:
            self._send_sc_notification(TEXT_CONFIRM_SUCCEED, res.text)

    def _send_sc_notification(self, text, desp=''):
        """Send sc notification."""
        for sckey in self.config.sckeys:
            res = requests.get(SC_URL.format(sckey, quote(text), quote(desp)))
            print(res.content)
