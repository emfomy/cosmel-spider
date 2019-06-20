# -*- coding: utf-8 -*-

import os

import psycopg2
import scrapy
import sshtunnel

from utils.logging import *

class Db:

    def __init__(self, spider):
        config = spider.settings.get('CONFIG')
        logger().success(f'Connecting Database ... {config["db_host"]} :: {config["db_name"]}')
        self.tunnel = sshtunnel.SSHTunnelForwarder(
            (config['db_host'], 22),
            ssh_username=config['db_user'],
            ssh_pkey=config['db_pkey'],
            remote_bind_address=('127.0.0.1', 5432),
        )
        self.tunnel.start()
        logger().verbose(self.tunnel)

        self.pgdb = psycopg2.connect(
            dbname=config['db_name'],
            user=config['db_user'],
            password=config['db_password'],
            host='localhost',
            port=self.tunnel.local_bind_port,
        )

        self.pgcur = self.pgdb.cursor()

    def __del__(self):
        logger().success('Closing Database ...')
        try:
            self.pgcur.close()
            self.pgdb.close()
        except Exception as e:
            logger().error(exceptstr(e))
        finally:
            self.tunnel.close()

    def execute(self, *args, **kwargs):
        return self.pgcur.execute(*args, **kwargs)

    def fetchall(self, *args, **kwargs):
        return self.pgcur.fetchall(*args, **kwargs)

    def commit(self, *args, **kwargs):
        return self.pgdb.commit(*args, **kwargs)
