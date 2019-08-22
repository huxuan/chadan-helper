#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: util.py
Author: huxuan
Email: i(at)huxuan.org
Description: Utilities used for chadan helper.
"""
from datetime import datetime


def within_time_range(start_time, end_time, now_time=None):
    """Check whether time is in a specific time range."""
    now_time = now_time or datetime.utcnow().time()
    if start_time < end_time:
        return start_time <= now_time <= end_time
    return now_time >= start_time or now_time <= end_time
