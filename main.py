#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for HuaFei Predator.
"""
from huafei_predator import HuaFeiPredator


def main():
    """Main process to trigger HuaFei Predator."""
    app = HuaFeiPredator()
    app.run()


if __name__ == '__main__':
    main()
