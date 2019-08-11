#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for chadan helper.
"""
from chadan_helper import ChadanHelper


def main():
    """Main process to trigger ChadanHelper."""
    chadan = ChadanHelper()
    chadan.login()
    chadan.get_orders()


if __name__ == '__main__':
    main()
