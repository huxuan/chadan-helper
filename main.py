#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for chadan helper.
"""
from datetime import datetime
import random

from python_json_config import ConfigBuilder

from chadan_helper import ChadanHelper

CONFIG_FILENAME = 'config.json'
TIME_FORMAT = '%H:%M'


def main():
    """Main process to trigger ChadanHelper."""
    config = parse_config()
    chadan = ChadanHelper(config)
    chadan.login()
    chadan.get_orders()


def parse_config():
    """Parse Configuration."""
    builder = ConfigBuilder()
    config = builder.parse_config(CONFIG_FILENAME)
    config.confirm_delay = config.confirm_delay or random.randint(500, 600)
    config.options = [option for option in config.options if option[1]]
    config.sleep_duration = config.sleep_duration or 0.5
    config.startTime = datetime.strptime(config.startTime, TIME_FORMAT).time()
    config.endTime = datetime.strptime(config.endTime, TIME_FORMAT).time()
    return config


if __name__ == '__main__':
    main()
