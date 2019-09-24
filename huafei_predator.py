#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: HuaFeiPredator.py
Author: huxuan
Email: i(at)huxuan.org
Description: Entrance for HuaFei Predator.
"""
from concurrent.futures import ThreadPoolExecutor
import time

from chadan_helper import ChadanHelper
from config import Config
from notification import Notification
from util import within_time_range
import common

TEXT_EXIT = 'HuaFeiPredator 将要退出啦'
TEXT_OFF_TIME = 'HuaFeiPredator 也要休息啦'
ERROR_UNKNOWN_PLATFORM_FORMAT = "Unknown Platform: {}"

OPERATORS = {
    'M': 'MOBILE',
    'U': 'UNICOM',
    'T': 'TELECOM',
    'S': 'SPECIAL'
}


class HuaFeiPredator():
    """Predator of HuaFei."""
    def __init__(self):
        super(HuaFeiPredator, self).__init__()
        self.accounts = {}
        self.config = Config()
        self.loop_status = True
        Notification.set(self.config)

    def run(self):
        """Trigger the Predator."""
        self._parse_accounts()
        self._get_orders()

    def _parse_accounts(self):
        """Parse the accounts."""
        for account in self.config.accounts:
            if account.platform.startswith(common.PLATFORM_CHADAN):
                self.accounts[account.platform] = ChadanHelper(account)
            else:
                raise ValueError(ERROR_UNKNOWN_PLATFORM_FORMAT.format(
                    account.platform))

    def _get_orders(self):
        """Get Orders"""
        executor = ThreadPoolExecutor(len(self.config.options))
        for option in self.config.options:
            future = executor.submit(self._get_orders_worker, *option)
            future.add_done_callback(lambda x: x.result())
        try:
            while True:
                time.sleep(self.config.sleep_duration)
        except KeyboardInterrupt:
            print(TEXT_EXIT)
            self.loop_status = False
            executor.shutdown(wait=False)

    def _get_orders_worker(self, value, amount, operators):
        """Worker to get orders."""
        total_operators = sum([
            len(operators.get(platform, ''))
            for platform in self.accounts
        ])
        while self.loop_status and amount > 0:
            if self.config.check_time and \
               not within_time_range(self.config.start_time,
                                     self.config.end_time):
                print(TEXT_OFF_TIME)
                time.sleep(self.config.sleep_duration)
                continue
            for account in self.config.accounts:
                for operator in operators.get(account.platform, ''):
                    if self.loop_status and amount > 0 and \
                       operator in OPERATORS:
                        amount -= self.accounts[account.platform].get_order(
                            value, amount, OPERATORS[operator])
                    time.sleep(self.config.sleep_duration / total_operators)
