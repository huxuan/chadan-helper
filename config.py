#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: config.py
Author: huxuan
Email: i(at)huxuan.org
Description: Configuration module.
"""
import json
import os.path

from util import parse_time


class _Config():
    """Configuration Node."""
    def __init__(self, config_dict):
        self.__dict__.update(config_dict)
        for key in config_dict:
            if isinstance(config_dict[key], dict):
                self.__dict__[key] = _Config(config_dict[key])
            elif isinstance(config_dict[key], list):
                self.__dict__[key] = [
                    _Config(config_item)
                    if isinstance(config_item, dict) else config_item
                    for config_item in config_dict[key]
                ]

    def __getattr__(self, key):
        """Get value with dynamic key."""
        return self.__dict__.get(key, None)

    def __setattr__(self, key, value):
        """Set value with dynamic key."""
        self.__dict__[key] = _Config(value) \
            if isinstance(value, dict) else value


class Config(_Config):
    """General Configuration."""
    def __init__(self, config):
        if os.path.isfile(config):
            config = json.load(open(config))
        elif isinstance(config, str):
            config = json.loads(config)
        super(Config, self).__init__(config)

        # Default value.
        self.options = [option for option in self.options if option[1]]
        self.sleep_duration = self.sleep_duration or 1.0
        self.start_time = parse_time(self.start_time)
        self.end_time = parse_time(self.end_time)
