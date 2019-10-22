#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: notification.py
Author: huxuan
Email: i(at)huxuan.org
Description: Notification module.
"""
import requests

SC_URL = 'https://sc.ftqq.com/{}.send'
WP_URL = 'http://wxpusher.zjiecode.com/api/send/message'
CHADAN_ORDER_URL = 'http://www.chadan.cn/wang/order'


TITLE_SC_CONFIRM_ORDER_FORMAT = '{mobile}{msg}'
TITLE_SC_GET_ORDER_FORMAT = '{mobile} {province}{operator} {value}'
TITLE_WP_CONFIRM_ORDER = '## 话费单已上报！'
TITLE_WP_GET_ORDER = '## 话费单来啦~'
CONTENT_ORDER_FORMAT = """
### **{mobile}** *{province}{operator}* *{value}*
[来源] {platform} {username}
"""


class Notification():  # pylint: disable=unused-variable
    """Notification module."""

    @classmethod
    def set(cls, config):
        """Set config in notification module."""
        cls.sckeys = config.sckeys
        cls.wpuids = config.wxpusher_uids
        cls.wptoken = config.wxpusher_token

    @classmethod
    def send_confirm_order(cls, args):
        """Send confirming order notification."""
        title_sc = TITLE_SC_CONFIRM_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        cls._send_sc(title_sc, content)
        cls._send_wp(TITLE_WP_CONFIRM_ORDER, content, CHADAN_ORDER_URL)

    @classmethod
    def send_get_order(cls, args):
        """Send getting order notification."""
        title_sc = TITLE_SC_GET_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        cls._send_sc(title_sc, content)
        cls._send_wp(TITLE_WP_GET_ORDER, content, CHADAN_ORDER_URL)

    @classmethod
    def _send_sc(cls, text, desp):
        """Send ServerChain notification."""
        for sckey in cls.sckeys:
            payload = {
                'text': text,
                'desp': desp
            }
            try:
                res = requests.get(SC_URL.format(sckey), params=payload)
                print(res.json())
            except Exception as exc: # pylint: disable=broad-except
                print("Fail to send ServerChain notification: {}".format(exc))

    @classmethod
    def _send_wp(cls, title, content, url=None):
        """Send WxPusher notification."""
        payload = {
            'appToken': cls.wptoken,
            'content': '{}{}'.format(title, content),
            'contentType': 3,
            'uids': cls.wpuids,
            'url': url
        }
        try:
            res = requests.post(WP_URL, json=payload)
            print(res.json())
        except Exception as exc: # pylint: disable=broad-except
            print("Fail to send WxPusher notification: {}".format(exc))
