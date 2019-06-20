#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2019'

import os

def fracstr(i, total):
    return f'{i+1:0{len(str(total))}}/{total}'

def pctstr(i, total):
    return f'{i/total*100:04.1f}%'

def ratiostr(i, total):
    return f'{fracstr(i, total)} = {pctstr(i, total)}'

def ordinal(n):
    return f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'

def mkdirs_file(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
