#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: util.py
Author: huxuan
Email: i(at)huxuan.org
Description: Utilities used for chadan helper.
"""
from datetime import datetime
from datetime import time


def within_time_range(startTime, endTime, nowTime=None):
    """Check whether time is in a specific time range."""
    nowTime = nowTime or datetime.utcnow().time()
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    return nowTime >= startTime or nowTime <= endTime