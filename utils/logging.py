#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2019'

import inspect as _inspect
import logging as _logging
import os as _os

import coloredlogs as _coloredlogs
import verboselogs as _verboselogs

_fmt = '%(asctime)s %(name)32.32s:%(lineno)-4d %(levelname)8s %(message)s'
_field_styles = {
    'asctime': {'color': 'green', 'faint': True},
    'name': {'color': 'cyan', 'faint': True},
    'levelname': {'color': 'black', 'bold': True},
}
_level_styles = {
    'spam': {'color': 'magenta', 'faint': True},
    'debug': {'color': 'blue'},
    'verbose': {'color': 'magenta'},
    'info': {'color': 'cyan'},
    'notice': {'background': 'cyan', 'bold': True},
    'warning': {'background': 'yellow', 'bold': True},
    'success': {'color': 'green', 'bold': True},
    'error': {'color': 'red', 'bold': True},
    'critical': {'background': 'red', 'bold': True},
}

_verboselogs.install()
_coloredlogs.install(level=5, fmt=_fmt, level_styles=_level_styles, field_styles=_field_styles)

def logger():
    frm = _inspect.stack()[1]
    mod = _inspect.getmodule(frm[0])
    name = getattr(mod, '__name__', '')
    return _logging.getLogger(name)

def exceptstr(e):
    return f'{e.__class__.__name__}: {e}'

def demonstrate_logging():
    for name in _level_styles:
        level = _coloredlogs.level_to_number(name)
        logger().log(level, f'message with level {name} ({level})')

if __name__ == '__main__':
    demonstrate_logging()
