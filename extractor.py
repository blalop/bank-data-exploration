#!/usr/bin/env python3

import argparse
import glob
import re

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
        self.read_pdf()

    def read_pdf(self):
        with open(self.filename, "rb") as f:
            pdf = '\n'.join(pdftotext.PDF(f))
            self.operations = Report.OPS_REGEX.findall(pdf)
            self.year = Report.YEAR_REGEX.findall(pdf)[0]

    def to_dataframe(self):
        df = pd.DataFrame(self.operations, columns=Report.COLUMN_NAMES)
        df.concept = df.concept.apply(lambda x: Report.TRIM_REGEX.sub(' ', x).strip())
        df.subconcept = df.subconcept.apply(lambda x: Report.TRIM_REGEX.sub(' ', x).strip())
        df.date = pd.to_datetime(df.date + '/' + self.year, dayfirst=True)
        df.value_date = pd.to_datetime(df.value_date + '/' + self.year, dayfirst=True)
        df.amount = pd.to_numeric(df.amount.apply(lambda x: x.replace('.', '').replace(',', '.')))
        df.balance = pd.to_numeric(df.balance.apply(lambda x: x.replace('.', '').replace(',', '.')))
        return df


def parse_args():
    parser = argparse.ArgumentParser(description='Extracts data from BBVA reports PDF files to a CSV')
    parser.add_argument('dirname', help='Directory of the PDF files')
    return parser.parse_args()


def main():
    args = parse_args()
    filenames = glob.glob(f'{args.dirname}/*.pdf')
    reports = map(Report, filenames)
    dataframes = map(lambda r: r.to_dataframe(), reports)
    dataframe = pd.concat(dataframes)
    dataframe.to_csv('movements.csv', index=False, sep='|')


if __name__ == '__main__':
    main()
