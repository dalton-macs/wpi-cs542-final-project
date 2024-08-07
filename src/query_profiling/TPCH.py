import sqlite3
import pandas as pd
import time


class TPCHQueries:
    """
    Custom class for running and profiling TPC-H queries.
    """

    def __init__(self):
        """
        Create connection to database
        """
        self.conn = sqlite3.connect('../../data/TPCH.db')

    def profile_query(self, query_name, is_View=False):
        """
        Profiles the query specified by query_name by return the result and execution time in seconds
        """
        start = time.time()
        with open('../../data/queries/{}'.format(query_name), 'r') as query:
            if is_View:
                self.conn.cursor().execute(query.read())
                res = ""
            else:
                res = pd.read_sql_query(query.read(), self.conn)
        end = time.time()
        return res, end - start

    def drop_view(self, view_name):
        self.conn.cursor().execute('DROP VIEW {}'.format(view_name))
