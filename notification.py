#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: notification.py
Author: huxuan
Email: i(at)huxuan.org
Description: Notification module.
"""
from urllib.parse import quote

import requests

SC_URL = 'https://sc.ftqq.com/{}.send?text={}&desp={}'
TITLE_CONFIRM_ORDER_FORMAT = '[HF]报单{mobile}{msg}'
TITLE_GET_ORDER_FORMAT = '[HF]抢单 {mobile} {operator} {value}元'
CONTENT_ORDER_FORMAT = """
## 充值信息
- 充值号码： **{mobile}**
- 归属地： **{operator}**
- 面值： **{value}**

## 话费单来源
- 平台： {platform}
- 账户（*非充值号码！*）： {username}
"""


class Notification():  # pylint: disable=unused-variable
    """Notification module."""

    @classmethod
    def set_sckeys(cls, sckeys):
        """Set sckeys in notification module."""
        cls.sckeys = sckeys

    @classmethod
    def send(cls, title, content=''):
        """Universal interface for sending notification."""
        cls._send_sc(title, content)

    @classmethod
    def send_confirm_order(cls, args):
        """Send confirming order notification."""
        title = TITLE_CONFIRM_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        cls.send(title, content)

    @classmethod
    def send_get_order(cls, args):
        """Send getting order notification."""
        title = TITLE_GET_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        cls.send(title, content)

    @classmethod
    def _send_sc(cls, text, desp):
        """Send ServerChain notification."""
        for sckey in cls.sckeys:
            res = requests.get(SC_URL.format(sckey, quote(text), quote(desp)))
            print(res.json())
