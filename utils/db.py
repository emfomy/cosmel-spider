# -*- coding: utf-8 -*-

import os

import pymysql
import scrapy

from utils.logging import *

class Db:

    def __init__(self, spider):
        config = spider.settings.get('CONFIG')
        logger().success(f'Connecting Database ... {config["db_host"]} :: {config["db_name"]}')

        self.mydb = pymysql.connect(
            host=config['db_host'],
            database=config['db_name'],
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
        return self.mycur.execute(*args, **kwargs)

    def fetchall(self, *args, **kwargs):
        return self.mycur.fetchall(*args, **kwargs)

    def commit(self, *args, **kwargs):
        logger().success('Committing Database ...')
        return self.mydb.commit(*args, **kwargs)
