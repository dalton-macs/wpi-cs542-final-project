

import os
import logging
import sqlite3
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

LOG = logging.getLogger(__name__)


def get_numerical_fields() -> pd.DataFrame:
    """Gets all numerical fields and corresponding tables from TPCH."""
    conn = sqlite3.connect('../../data/tpch.db')

    tables = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table'", conn
    ).name.tolist()

    LOG.info(f"Tables: {tables}")

    pragma_list = []
    for table in tables:
        pdf = pd.read_sql_query(f"PRAGMA table_info({table})", conn)\
            [['name', 'type', 'pk']].rename(columns={'name': 'field'})

        pragma_list.append(
            pd.concat([
                pd.DataFrame({'table': [table]*pdf.shape[0]}),
                pdf
            ], axis = 1)
        )

    pragma_df = pd.concat(pragma_list).reset_index(drop=True)
    pragma_df['base_field'] = pragma_df['field'].apply(lambda x: x.split('_')[1])

    pks = pragma_df[pragma_df.pk != 0].base_field.unique().tolist()

    numerical_fields = pragma_df[(~pragma_df.base_field.isin(pks)) & 
                                 (pragma_df.type.isin(
                                     ['INTEGER', 'REAL', 'NUMERIC'])
                                )][['table', 'field', 'type']].reset_index(
                                    drop=True
                                )
    LOG.info(
        'Numerical Fields: '\
        f'{numerical_fields.apply(lambda x: f"{x.table}.{x.field}", axis = 1).tolist()}'
    )

    conn.close()

    return numerical_fields
