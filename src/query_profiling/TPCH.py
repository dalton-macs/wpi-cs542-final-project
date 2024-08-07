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

    def q2(self) -> (pd.DataFrame, float):
        start = time.time()
        res = pd.read_sql("SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment "
                          "FROM part, supplier, partsupp, nation, region "
                          "WHERE p_partkey = ps_partkey and s_suppkey = ps_suppkey and p_size = 15 and "
                          "p_type like '%BRASS' and s_nationkey = n_nationkey and n_regionkey = r_regionkey "
                          "and r_name = 'EUROPE' and "
                          "ps_supplycost = (SELECT min(ps_supplycost) FROM partsupp, supplier, nation, region "
                          "WHERE p_partkey = ps_partkey and s_suppkey = ps_suppkey and s_nationkey = n_nationkey "
                          "and n_regionkey = r_regionkey and r_name = 'EUROPE') "
                          "ORDER BY s_acctbal desc, n_name, s_name, p_partkey", self.conn)
        end = time.time()
        return res, end - start

    def q3(self) -> (pd.DataFrame, float):
        start = time.time()
        res = pd.read_sql(
            "SELECT l_orderkey, sum(l_extendedprice*(1-l_discount)) as revenue, o_orderdate, o_shippriority "
            "FROM customer, orders, lineitem "
            "WHERE c_mktsegment = 'BUILDING' and c_custkey = o_custkey and l_orderkey = o_orderkey "
            "and o_orderdate < date('1995-03-15') and l_shipdate > date('1995-03-15') "
            "GROUP BY l_orderkey, o_orderdate, o_shippriority "
            "ORDER BY revenue desc, o_orderdate", self.conn)
        end = time.time()
        return res, end - start

    def q4(self) -> (pd.DataFrame, float):
        start = time.time()
        res = pd.read_sql("SELECT o_orderpriority, count(*) as order_count "
                          "FROM orders "
                          "WHERE o_orderdate >= date('1993-07-01') and o_orderdate < date('1993-07-01', '3 month') "
                          "and EXISTS (select * FROM lineitem WHERE l_orderkey = o_orderkey and l_commitdate < l_receiptdate) "
                          "GROUP BY o_orderpriority "
                          "ORDER BY o_orderpriority", self.conn)
        end = time.time()
        return res, end - start

    def q5(self) -> (pd.DataFrame, float):
        start = time.time()
        res = pd.read_sql("SELECT n_name, sum(l_extendedprice * (1 - l_discount)) as revenue "
                          "FROM customer, orders, lineitem, supplier, nation, region "
                          "WHERE c_custkey = o_custkey and l_orderkey = o_orderkey and l_suppkey = s_suppkey "
                          "and c_nationkey = s_nationkey and s_nationkey = n_nationkey and n_regionkey = r_regionkey "
                          "and r_name = 'ASIA' and o_orderdate >= date('1994-01-01') and o_orderdate < date('1994-01-01', '1 year') "
                          "GROUP BY n_name "
                          "ORDER BY revenue DESC", self.conn)
        end = time.time()
        return res, end - start

    def q6(self) -> (pd.DataFrame, float):
        start = time.time()
        res = pd.read_sql("SELECT sum(l_extendedprice * l_discount) as revenue "
                          "FROM lineitem "
                          "WHERE l_shipdate >= date('1994-01-01') "
                          "AND l_shipdate < date('1994-01-01', '1 year') "
                          "AND l_discount BETWEEN 0.05 AND 0.07 "
                          "AND l_quantity < 24", self.conn)
        end = time.time()
        return res, end - start
