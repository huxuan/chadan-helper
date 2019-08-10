#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for chadan helper.
"""
import multiprocessing
import sys

from chadan_helper import ChadanHelper


def main():
    """Main process to trigger ChadanHelper."""
    chadan = ChadanHelper()
    chadan.login()
    chadan.get_orders()


if __name__ == '__main__':
    # Fix multiprocessing issue for windows executable.
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    main()
