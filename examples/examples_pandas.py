import os
import pandas as pd
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

if __name__ == '__main__':

    conn = sqlite3.connect('../data/tpch.db')
    cursor = conn.cursor()

    query = "select * from CUSTOMER limit 10;"

    df = pd.read_sql_query(query, conn)
    print(df)

    conn.close()
