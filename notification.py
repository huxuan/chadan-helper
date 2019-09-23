#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: notification.py
Author: huxuan
Email: i(at)huxuan.org
Description: Notification module.
"""
import requests

import common

SC_URL = 'https://sc.ftqq.com/{}.send'
WXPUSHER_URL = 'http://wxpusher.zjiecode.com/api/send/message'
CHADAN_ORDER_URL = 'http://www.chadan.cn/wang/order'
CHADAN_SPECIAL_URL = 'http://www.chadan.cn/wang/specialFareMoblie'


TITLE_CONFIRM_ORDER_FORMAT = '[HF]报单{mobile}{msg}'
TITLE_GET_ORDER_FORMAT = '[HF]抢单 {mobile} {province}{operator} {value}元'
CONTENT_ORDER_FORMAT = """
## 充值信息
- 充值号码： **{mobile}**
- 归属地： **{province}{operator}**
- 面值： **{value}**

## 话费单来源
- 平台： {platform}
- 账户（*非充值号码！*）： {username}
"""


class Notification():  # pylint: disable=unused-variable
    """Notification module."""

    @classmethod
    def set(cls, config):
        """Set config in notification module."""
        cls.sckeys = config.sckeys
        cls.wxpusher_uids = config.wxpusher_uids
        cls.wxpusher_token = config.wxpusher_token

    @classmethod
    def send_confirm_order(cls, args):
        """Send confirming order notification."""
        title = TITLE_CONFIRM_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        cls._send_sc(title, content)
        cls._send_wxpusher(content, args)

    @classmethod
    def send_get_order(cls, args):
        """Send getting order notification."""
        title = TITLE_GET_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        if args['platform'].startswith(common.PLATFORM_CHADAN):
            url = CHADAN_SPECIAL_URL if args['province'] == '全国' \
                  else CHADAN_ORDER_URL
        cls._send_sc(title, content)
        cls._send_wxpusher(content, url)

    @classmethod
    def _send_sc(cls, text, desp):
        """Send ServerChain notification."""
        for sckey in cls.sckeys:
            payload = {
                'text': text,
                'desp': desp
            }
            res = requests.get(SC_URL.format(sckey), params=payload)
            print(res.json())

    @classmethod
    def _send_wxpusher(cls, content, url=None):
        """Send WxPusher notification."""
        payload = {
            'appToken': cls.wxpusher_token,
            'content': content,
            'uids': cls.wxpusher_uids,
            'url': url
        }
        res = requests.post(WXPUSHER_URL, json=payload)
        print(res.json())
