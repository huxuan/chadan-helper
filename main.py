#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for chadan helper.
"""
from chadan_helper import ChadanHelper
from config import Config
from notification import Notification

CONFIG_FILENAME = 'config.json'


def main():
    """Main process to trigger ChadanHelper."""
    config = Config(CONFIG_FILENAME)
    Notification.set_sckeys(config.sckeys)
    chadan = ChadanHelper(config)
    chadan.login()
    chadan.get_orders()


if __name__ == '__main__':
    main()
