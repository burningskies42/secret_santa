import sqlite3
from sqlite3 import Error

import pandas as pd
from loguru import logger


class Connection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(self.db_file)
            logger.info(f"Connected to {self.db_file}")
        except Error as e:
            logger.error(e)

    def disconnect(self):
        """terminate database connection
        """
        self.conn.close()
        logger.info("Closing connection")

    def execute(self, query, params=None):
        """execute query on database

        Args:
            query (string): sql query to run
            fetch (bool, optional): whether the query should return the cursor. Defaults to False.

        """
        assert self.conn is not None, "Not connected"
        cur = self.conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        self.conn.commit()
        cur.close()

    def query(self, query, params=None):
        """execute query and return the resulting data

        Args:
            query (string): sql query to execute

        Returns:
            list: resulting dataset from query
        """
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()

        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data

    def query_dataframe(self, query, params=None):
        return pd.DataFrame(self.query(query, params=params))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
