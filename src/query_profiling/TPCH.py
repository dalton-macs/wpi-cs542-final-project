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

    def q1(self) -> (pd.DataFrame, float):
        start = time.time()
        res = pd.read_sql("SELECT l_returnflag, l_linestatus, sum(l_quantity) as sum_qty,"
                          "sum(l_extendedprice) as sum_base_price, sum(l_extendedprice*(1-l_discount)) as sum_disc_price, "
                          "sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge, avg(l_quantity) as avg_qty, "
                          "avg(l_extendedprice) as avg_price, avg(l_discount) as avg_disc, count(*) as count_order "
                          "FROM lineitem "
                          "WHERE l_shipdate <= date('1998-12-01', '-90 day') "
                          "GROUP BY l_returnflag, l_linestatus "
                          "ORDER BY l_returnflag, l_linestatus", self.conn)
        end = time.time()
        return res, end - start
