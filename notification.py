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
WXPUSHER_URL = 'http://wxmsg.dingliqc.com/send'
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
    def set_sckeys(cls, sckeys):
        """Set sckeys in notification module."""
        cls.sckeys = sckeys

    @classmethod
    def set_wxpusher_keys(cls, wxpusher_keys):
        """Set WxPusher Keys in to notification module."""
        cls.wxpusher_keys = wxpusher_keys

    @classmethod
    def send_confirm_order(cls, args):
        """Send confirming order notification."""
        title = TITLE_CONFIRM_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        cls._send_sc(title, content)
        cls._send_wxpusher(title, content, args)

    @classmethod
    def send_get_order(cls, args):
        """Send getting order notification."""
        title = TITLE_GET_ORDER_FORMAT.format(**args)
        content = CONTENT_ORDER_FORMAT.format(**args)
        cls._send_sc(title, content)
        cls._send_wxpusher(title, content, args)

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
    def _send_wxpusher(cls, title, content, args):
        """Send WxPusher notification."""
        url = 'nourl'
        if args['platform'].startswith(common.PLATFORM_CHADAN):
            url = CHADAN_SPECIAL_URL if args['province'] == '全国' \
                  else CHADAN_ORDER_URL
        payload = {
            'title': title,
            'msg': content,
            'userIds': cls.wxpusher_keys,
            'url': url
        }
        res = requests.get(WXPUSHER_URL, params=payload)
        print(res.json())
