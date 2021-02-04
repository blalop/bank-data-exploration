
import pandas as pd
import numpy as np

import accountman.extractor as extr


def _group_by_month(dataframe: pd.DataFrame, aggregation_dict: dict):
    grouped_dataframe = dataframe.set_index('date').groupby(
        pd.Grouper(freq='M')).aggregate(aggregation_dict)
    grouped_dataframe.index = grouped_dataframe.index.map(
        lambda x: x if isinstance(x, str) else x.strftime('%Y-%m'))
    return grouped_dataframe


def movements() -> pd.DataFrame:
    return extr.extract_directory('bbva_reports').sort_values('date')


def payroll_movements() -> pd.DataFrame:
    m = movements()
    return m[m['concept'].str.contains('NOMINA')]


def spending() -> pd.DataFrame:
    return movements().query('amount < 0')


def incoming() -> pd.DataFrame:
    return movements().query('amount > 0')


def spending_by_month() -> pd.DataFrame:
    return _group_by_month(spending(), {'amount': np.sum})


def incoming_by_month() -> pd.DataFrame:
    return _group_by_month(incoming(), {'amount': np.sum})


def spending_incoming_by_month() -> pd.DataFrame:
    spending_renamed = spending_by_month()
    incoming_renamed = incoming_by_month()
    return pd.concat([spending_renamed, incoming_renamed])


def diff_by_month() -> pd.DataFrame:
    spending_renamed = spending_by_month()
    incoming_renamed = incoming_by_month()
    return spending_renamed + incoming_renamed


def spending_by_concept() -> pd.DataFrame:
    return spending().groupby('concept').amount.sum()


def incoming_by_concept() -> pd.DataFrame:
    return incoming().groupby('concept').amount.sum()


def spending_incoming_by_concept() -> pd.DataFrame:
    spending_renamed = spending_by_concept().rename('spending')
    incoming_renamed = incoming_by_concept().rename('incoming')
    return pd.concat([spending_renamed, incoming_renamed], axis=1)


def spending_abs() -> pd.DataFrame:
    return spending().amount.abs()


def spending_by_concept_sorted() -> pd.DataFrame:
    return spending_by_concept().abs().sort_values()
