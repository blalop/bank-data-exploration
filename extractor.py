#!/usr/bin/env python3

import argparse
import glob
import re
import sqlite3

import pandas as pd
import pdftotext


class Report:

    COLUMN_NAMES = ['date', 'value_date', 'concept', 'amount', 'balance', 'card', 'subconcept']

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

    def __init__(self, filename):
        self.filename = filename
        self._read_pdf()

    def _read_pdf(self):
        with open(self.filename, "rb") as f:
            pdf = '\n'.join(pdftotext.PDF(f))
            self.operations = Report.OPS_REGEX.findall(pdf)
            self.year = Report.YEAR_REGEX.findall(pdf)[0]

    @staticmethod
    def _trim_str(col):
        return col.apply(lambda x: Report.TRIM_REGEX.sub(' ', x).strip())

    @ staticmethod
    def _decimal_separator(col):
        return pd.to_numeric(col.apply(lambda x: x.replace('.', '').replace(',', '.')))

    def _format_date(self, col):
        return pd.to_datetime(col + '/' + self.year, dayfirst=True)

    def to_dataframe(self):
        df = pd.DataFrame(self.operations, columns=Report.COLUMN_NAMES)
        df.concept = self._trim_str(df.concept)
        df.subconcept = self._trim_str(df.subconcept)
        df.date = self._format_date(df.date)
        df.value_date = self._format_date(df.value_date)
        df.amount = self._decimal_separator(df.amount)
        df.balance = self._decimal_separator(df.balance)
        return df


def extract(dirname):
    filenames = glob.glob(f'{dirname}/*.pdf')
    reports = map(Report, filenames)
    dataframes = map(lambda r: r.to_dataframe(), reports)
    dataframe = pd.concat(dataframes)
    return dataframe


def main(dirname, output_format):
    dataframe = extract(dirname)
    if output_format == 'csv':
        dataframe.to_csv('movements.csv', sep='|', index=False)
    elif output_format == 'sql':
        dataframe.to_sql('MOVEMENTS', sqlite3.connect('movements.db'), if_exists='replace', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts data from BBVA reports PDF files')
    parser.add_argument('dirname', help='Directory of the PDF files')
    parser.add_argument('output_format', help='Format of the output', choices=['sql', 'csv'])
    args = parser.parse_args()
    main(args.dirname, args.output_format)
