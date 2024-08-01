import os
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

if __name__ == '__main__':

    conn = sqlite3.connect('../data/tpch.db')
    cursor = conn.cursor()

    query = "select * from CUSTOMER limit 10;"

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)

    cursor.close()
    conn.close()
