# -*- coding: utf-8 -*-

import os

import psycopg2
import scrapy

from utils.logging import *

class Db:

    def __init__(self, spider):
        config = spider.settings.get('CONFIG')
        logger().success(f'Connecting Database ... {config["db_host"]} :: {config["db_name"]}')

        self.pgdb = psycopg2.connect(
            host=config['db_host'],
            dbname=config['db_name'],
            user=config['db_user'],
            password=config['db_password'],
        )

        self.pgcur = self.pgdb.cursor()

    def __del__(self):
        logger().success('Closing Database ...')
        try:
            self.pgcur.close()
            self.pgdb.close()
        except Exception as e:
            logger().error(exceptstr(e))

    def execute(self, *args, **kwargs):
        return self.pgcur.execute(*args, **kwargs)

    def fetchall(self, *args, **kwargs):
        return self.pgcur.fetchall(*args, **kwargs)

    def commit(self, *args, **kwargs):
        return self.pgdb.commit(*args, **kwargs)
