#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import warnings

import pymysql
import scrapy

from utils.logging import *

class Db:

    def __init__(self, spider):
        config = spider.settings.get('CONFIG')
        logger().success(f'Connecting Database ... {config["db_host"]}')

        self.mydb = pymysql.connect(
            host=config['db_host'],
            user=config['db_user'],
            password=config['db_password'],
        )

        self.mycur = self.mydb.cursor()

    def __del__(self):
        logger().success('Closing Database ...')
        try:
            self.mycur.close()
            self.mydb.close()
        except Exception as e:
            logger().error(exceptstr(e))

    def execute(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('error', category=pymysql.Warning)
            return self.mycur.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('error', category=pymysql.Warning)
            return self.mycur.executemany(*args, **kwargs)

    def fetchone(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('error', category=pymysql.Warning)
            return self.mycur.fetchone(*args, **kwargs)

    def fetchall(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('error', category=pymysql.Warning)
            return self.mycur.fetchall(*args, **kwargs)

    def commit(self, *args, **kwargs):
        logger().success('Committing Database ...')
        with warnings.catch_warnings():
            warnings.simplefilter('error', category=pymysql.Warning)
            return self.mydb.commit(*args, **kwargs)
