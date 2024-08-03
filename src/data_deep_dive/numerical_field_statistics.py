import os
import logging
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_numerical_fields


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

LOG = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)


def compute_statistics(df, column):
    data = df[column]
    na_count = data.isna().sum()

    data.dropna(inplace=True)

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    relative_min = q1 - 1.5 * iqr
    relative_max = q3 + 1.5 * iqr

    stats_dict = {
        'count': [data.count()],
        'mean': [data.mean()],
        'median': [data.median()],
        'mode': [data.mode().iloc[0] if not data.mode().empty else None],
        'min': [data.min()],
        'max': [data.max()],
        'std': [data.std()],
        'cardinality': [data.nunique()],
        'q1': [q1],
        'q3': [q3],
        'iqr': [iqr],
        'relative_min': [relative_min],
        'relative_max': [relative_max],
        'na_count': [na_count]
    }
    return stats_dict


def plot_distribution(df: pd.DataFrame, 
                      table: str, 
                      field: str, 
                      plot_dir: str) -> None:

    plt.figure(figsize=(10, 5))
    sns.histplot(df[field], kde=True)
    plt.title(f'Histogram of {field} in {table}')
    plt.xlabel(field)
    plt.ylabel('Frequency')
    plt.savefig(f'{plot_dir}/{table}_{field}_histogram.png')
    # plt.show()
    plt.close()
    
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=df[field])
    plt.title(f'Box Plot of {field} in {table}')
    plt.xlabel(field)
    plt.savefig(f'{plot_dir}/{table}_{field}_boxplot.png')
    # plt.show()
    plt.close()


def generate_numerical_statistics(save_path: str,
                                  make_plots: bool = False) -> pd.DataFrame:

    conn = sqlite3.connect('../../data/tpch.db')

    numerical_fields_df = get_numerical_fields()

    stats_list = []
    for index, row in numerical_fields_df.iterrows():
        table = row['table']
        field = row['field']
        
        LOG.info(f"Processing {table}.{field}")
        
        numerical_data = pd.read_sql_query(f"SELECT {field} FROM {table}", conn)
        stats = compute_statistics(numerical_data, field)
        
        stats_list.append(
            pd.DataFrame({'table': table, 'field': field, **stats})
        )

        if make_plots:
            plot_dir = os.path.join(os.path.dirname(save_path), 'plots')
            if not os.path.exists(plot_dir):
                os.makedirs(plot_dir)
            plot_distribution(numerical_data, table, field, plot_dir)

    stats_df = pd.concat(stats_list).reset_index(drop=True)
    stats_df.set_index(['table', 'field'], inplace=True)

    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    stats_df.to_csv(save_path)

    conn.close()

if __name__ == "__main__":
    generate_numerical_statistics(save_path = 
                                  '../../data/data_deep_dive/numerical_fields_statistics.csv',
                                  make_plots = True)
