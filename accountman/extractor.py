

import glob
import logging
import re

import pandas as pd
import pdftotext


logger = logging.getLogger(__name__)


class Report:
    COLUMN_NAMES = ['date', 'value_date', 'concept',
                    'amount', 'balance', 'card', 'subconcept']

    YEAR_REGEX = re.compile(r'EXTRACTO DE \w* (\d{4})', re.MULTILINE)

    OPS_REGEX = re.compile(
        r'''^
        (\d\d/\d\d) #date
        \s
        (\d\d/\d\d) #value date
        \s*
        ([A-ZÑÁÉÍÓÚÜ\'\,\.\:\s]+) #concept
        \s*
        (-?\d*.?\d*,\d*) #amount of the movement
        \s*
        (\d*.?\d*,\d*) #balance after movement
        \s*
        (\d*) # credit card number
        \s*
        ([\d\wÑÁÉÍÓÚÜ \.\,\:\*\'\-\/\(\)]*) # subconcept
        $''',
        re.MULTILINE | re.IGNORECASE | re.VERBOSE
    )

    TRIM_REGEX = re.compile(r'\s+')

    def __init__(self, filename: str):
        self.filename = filename

        pdf_text = self._read_pdf()
        self.operations = Report.OPS_REGEX.findall(pdf_text)
        self.year = int(Report.YEAR_REGEX.findall(pdf_text)[0])

    def _read_pdf(self) -> str:
        with open(self.filename, 'rb') as f:
            return '\n'.join(pdftotext.PDF(f))

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.operations, columns=Report.COLUMN_NAMES)
        df.concept = _trim_str(df.concept)
        df.subconcept = _trim_str(df.subconcept)
        df.date = _format_date(df.date, self.year)
        df.value_date = _format_date(df.value_date, self.year)
        df.amount = _decimal_separator(df.amount)
        df.balance = _decimal_separator(df.balance)
        return df


def _trim_str(col: pd.Series) -> pd.Series:
    return col.apply(lambda x: Report.TRIM_REGEX.sub(' ', x).strip())


def _decimal_separator(col: pd.Series) -> pd.Series:
    return pd.to_numeric(col.apply(lambda x: x.replace('.', '').replace(',', '.')))


def _format_date(col: pd.Series, year: int) -> pd.Series:
    return pd.to_datetime(col + '/' + str(year), dayfirst=True)


def extract_file(filename: str) -> pd.DataFrame:
    logger.debug(f'Extracting from file "{filename}"')
    report = Report(filename)
    return report.to_dataframe()


def extract_directory(dirname: str) -> pd.DataFrame:
    logger.debug(f'Extracting from directory "{dirname}"')
    filenames = glob.glob(f'{dirname}/*.pdf')
    reports = map(Report, filenames)
    dataframes = map(lambda r: r.to_dataframe(), reports)
    return pd.concat(dataframes)
