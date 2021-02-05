import logging

import pandas as pd
import numpy as np

import accountman.extractor as extr


logger = logging.getLogger(__name__)


def _group_by_month(df: pd.DataFrame, aggr_dict: dict) -> pd.DataFrame:
    grouped_df = df.set_index('date').groupby(
        pd.Grouper(freq='M')).aggregate(aggr_dict)
    grouped_df.index = grouped_df.index.map(
        lambda x: x if isinstance(x, str) else x.strftime('%Y-%m'))
    return grouped_df


class Calculator:
    def __init__(self, dir: str) -> None:
        self.dir = dir
        self.update_movements()

    def update_movements(self) -> None:
        self.movements = extr.extract_directory(self.dir).sort_values('date')
        logger.info(f'Found {len(self.movements.index)} movements')

    def salary_movements(self) -> pd.DataFrame:
        return self.movements[self.movements['concept'].str.contains('NOMINA')]

    def spending(self) -> pd.DataFrame:
        return self.movements.query('amount < 0')

    def incoming(self) -> pd.DataFrame:
        return self.movements.query('amount > 0')

    def spending_by_month(self) -> pd.DataFrame:
        return _group_by_month(self.spending(), {'amount': np.sum})

    def incoming_by_month(self) -> pd.DataFrame:
        return _group_by_month(self.incoming(), {'amount': np.sum})

    def combined_by_month(self) -> pd.DataFrame:
        spending_renamed = self.spending_by_month()
        incoming_renamed = self.incoming_by_month()
        return pd.concat([spending_renamed, incoming_renamed])

    def diff_by_month(self) -> pd.DataFrame:
        return self.spending_by_month() + self.incoming_by_month()

    def spending_by_concept(self) -> pd.DataFrame:
        return self.spending().groupby('concept').amount.sum()

    def incoming_by_concept(self) -> pd.DataFrame:
        return self.incoming().groupby('concept').amount.sum()

    def combined_by_concept(self) -> pd.DataFrame:
        spending_renamed = self.spending_by_concept().rename('spending')
        incoming_renamed = self.incoming_by_concept().rename('incoming')
        return pd.concat([spending_renamed, incoming_renamed], axis=1)

    def spending_abs(self) -> pd.DataFrame:
        return self.spending().amount.abs()

    def spending_by_concept_sorted(self) -> pd.DataFrame:
        return self.spending_by_concept().abs().sort_values()
