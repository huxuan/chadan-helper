#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for chadan helper.
"""
import json
import multiprocessing
import sys

from chadan_helper import ChadanHelper

CONFIG_FILENAME = 'config.json'


def main():
    """Main process to trigger ChadanHelper."""
    with open(CONFIG_FILENAME) as config_file:
        config = json.load(config_file)

        username = config['Username']
        password = config['Password']
        options = config['Options']
        pool_limit = config['PoolLimit']
        sleep_duration = config['SleepDuration']

        chadan = ChadanHelper(username, password, options, pool_limit,
                              sleep_duration)
        chadan.login()
        chadan.get_orders()


if __name__ == '__main__':
    # Fix multiprocessing issue for windows executable.
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    main()
