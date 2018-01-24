#!/bin/env python
# -*- coding: utf-8 -*-
from gevent.monkey import patch_all

patch_all()

import time
import logging

ora_con_dict = {
    "schema": "127.0.0.1:1521/orcl",
    "user": "test",
    "passwd": "testpass"
}


pg_con_dict = {
    "host": "127.0.0.1",
    "port": "5432",
    "database": "postgres",
    "user": "postgres",
    "password": "testpass"
}

mysql_con_dict = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "testdb",
    "user": "test",
    "password": "testpass"
}


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(levelname)s]: [%(module)s.%(funcName)s()]: %(message)s')
LOGGER = logging.getLogger()

# Utils Part
# ===============================================================#
# from __future__ import generators    #needs to be at the top of your module
def ResultIter(cursor, arraysize=1000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for tup in results:
            yield tup

def ResultSetIter(cursor, arraysize=1000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        yield results

def ResDictIter(cursor, arraysize=1000):
	'An iterator that uses fetchmany to keep memory usage down'
	columns = [desc[0] for desc in cursor.description]
	while True:
		results = cursor.fetchmany(arraysize)
		if not results:
			break
		for tup in results:
			yield dict(zip(columns, tup))

class PlumberConnBase(object):
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def execute(self, sql):
        self.cursor.execute(sql)

    def execute_with_commit(self, sql):
        self.execute(sql)
        self.db.commit()

    def find(self):
        for tup in ResultIter(self.cursor):
            yield tup

    def find_batch(self):
        for batch in ResultSetIter(self.cursor):
            yield batch

	def find_dict(self):
		for rdict in ResDictIter(self.cursor):
			yield rdict

# Oracle Part
# ===============================================================#
import os
# for oracle encoding
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import cx_Oracle

class OraPlumberConn(PlumberConnBase):

    def __init__(self, user, passwd, schema):
        super(OraPlumberConn, self).__init__()

        self.db = cx_Oracle.connect(user, passwd, schema)
        self.cursor = self.db.cursor()


# PostgreSQL Part
# ===============================================================#
import psycopg2

class PgPlumberConn(PlumberConnBase):
    def __init__(self, database=None, user=None, password=None, host=None, port=None):
        super(PgPlumberConn, self).__init__()

        self.db = psycopg2.connect(database=database,
                        user=user, password=password,
                        host=host, port=port)
        self.cursor = self.db.cursor()

    def execute_insert(self, insert_sql, values):
        #  insert_sql = 'insert into t (a, b) values {}'
        records_list_template = ','.join(['%s'] * len(values))
        insert_query = insert_sql.format(records_list_template)
        self.cursor.execute(insert_query, values)
        self.db.commit()

# MySQL Part
# ===============================================================#
import MySQLdb

class MySQLPlumberConn(PlumberConnBase):
    def __init__(self, database=None, user=None, password=None, host=None, port=None):
        super(MySQLPlumberConn, self).__init__()

        self.db = MySQLdb.connect(
                        host=host, port=port,
                        user=user, passwd=password,
                        db=database, charset = 'utf8'
                        )
        self.cursor = self.db.cursor()

# Process Part
# ===============================================================#
class ProcessPrint(object):
    def __init__(self):
        pass

    def handle(self, item):
        print(item)
        return True

class ProcessInsert(object):
    def __init__(self, plumberConn, insert_sql):
        self.plumberConn = plumberConn
        self.insert_sql = insert_sql
        pass

    def handle(self, item):
        self.plumberConn.execute_insert(self.insert_sql, item)
        return True

def call_main():
    rawsql = None
    try:
        import sys
        import getopt
        options, args = getopt.getopt(sys.argv[1:], "hr:", ['help', "raw="])
        for name, value in options:
            if name in ('-h', '--help'):
                print("error")
            elif name in ('-r', '--raw'):
                rawsql = value
    except getopt.GetoptError:
        print("error")

    ora_rawsql = "select * from test where rownum < 10"
    ora_conn = OraPlumberConn(
        user=ora_con_dict['user'],
        passwd=ora_con_dict['passwd'],
        schema=ora_con_dict['schema'])
    ora_conn.execute(ora_rawsql)

    pg_rawsql = "select * from test limit 10"
    pg_conn = PgPlumberConn(
        database=pg_con_dict['database'],
        user=pg_con_dict['user'],
        password=pg_con_dict['password'],
        host=pg_con_dict['host'],
        port=pg_con_dict['port'])
    pg_conn.execute(pg_rawsql)

    insert_sql = 'insert into test values {}'
    process = ProcessInsert(pg_conn, insert_sql)

    from gevent.pool import Pool
    p = Pool(4)
    for _d in p.imap(process.handle, ora_conn.find_batch()):
        pass

if __name__ == "__main__":
    call_main()
