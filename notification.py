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


class Notification():
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
    def _send_sc(cls, text, desp):
        """Send ServerChain notification."""
        for sckey in cls.sckeys:
            res = requests.get(SC_URL.format(sckey, quote(text), quote(desp)))
            print(res.json())
