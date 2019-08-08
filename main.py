#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for chadan helper.
"""
import multiprocessing
import random
import sys

from python_json_config import ConfigBuilder

from chadan_helper import ChadanHelper

CONFIG_FILENAME = 'config.json'


def main():
    """Main process to trigger ChadanHelper."""
    builder = ConfigBuilder()
    config = builder.parse_config(CONFIG_FILENAME)
    config.confirm_delay = config.confirm_delay or random.randint(500, 600)
    config.pool_limit = config.pool_limit or len(config.options)
    config.sleep_duration = config.sleep_duration or 1
    chadan = ChadanHelper(config)
    chadan.login()
    chadan.get_orders()


if __name__ == '__main__':
    # Fix multiprocessing issue for windows executable.
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    main()
