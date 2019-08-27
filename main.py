#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main.py
Author: huxuan
Email: i(at)huxuan.org
Description: Main entrance for HuaFei Predator.
"""
import json

from huafei_predator import HuaFeiPredator


def main():
    """Main process to trigger HuaFei Predator."""
    try:
        app = HuaFeiPredator()
    except FileNotFoundError:
        input('配置文件 `config.json` 不存在！按任意键退出...')
        return
    except json.JSONDecodeError:
        input('配置文件解析失败，请检查配置文件格式！按任意键退出...')
        return
    except Exception as exc:  # pylint: disable=broad-except
        print(exc)
        input('未知错误，请附带上述信息告知维护者。按任意键退出...')
        return
    try:
        app.run()
    except Exception as exc:  # pylint: disable=broad-except
        print(exc)
        input('未知错误，请附带上述信息告知维护者。按任意键退出...')


if __name__ == '__main__':
    main()
