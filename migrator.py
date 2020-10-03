#!/usr/bin/env python3

import os
import re
import sys

import pandas as pd
import pdftotext

DIRNAME = sys.argv[1] if len(sys.argv) == 2 else 'reports'

COLUMN_NAMES = ['date', 'value_date', 'concept',
                'amount', 'balance', 'card', 'subconcept']

PDF_REGEX = re.compile(
    r'^([\d][\d]/[\d][\d])\s([\d][\d]/[\d][\d])\s*([A-ZÑñÁáÉéÍíÓóÚúÜü\'\,\.\:\s]+)\s*(-?\d*.?\d*,\d*)\s*(\d*.?\d*,\d*)\s*(\d*)\s*([\d\wÑñÁáÉéÍíÓóÚúÜü \.\,\:\*\'\-\/\(\)]*)$',
    re.MULTILINE
)

REMOVE_WHITESPACES_REGEX = re.compile(r'\s+')


def read_pdf(filename):
    year = filename[:4]
    with open(os.path.join(DIRNAME, filename), "rb") as f:
        pdf = '\n'.join(pdftotext.PDF(f))
        operations = PDF_REGEX.findall(pdf)
        return pd.DataFrame(operations, columns=COLUMN_NAMES).assign(year=year)


def parse_df(df):
    df.concept = df.concept.apply(lambda x: REMOVE_WHITESPACES_REGEX.sub(' ', x).strip())
    df.subconcept = df.subconcept.apply(lambda x: REMOVE_WHITESPACES_REGEX.sub(' ', x).strip())
    df.date = pd.to_datetime(df.date + '/' + df.year, dayfirst=True)
    df.value_date = pd.to_datetime(df.value_date + '/' + df.year, dayfirst=True)
    df.amount = pd.to_numeric(df.amount.apply(lambda x: x.replace('.', '').replace(',', '.')))
    df.balance = pd.to_numeric(df.balance.apply(lambda x: x.replace('.', '').replace(',', '.')))
    return df.drop('year', axis=1)


filenames = [f for _, _, files in os.walk(DIRNAME) for f in files]
df = pd.concat(map(read_pdf, filenames))
parse_df(df).to_csv('movements.csv', index=False, sep='|')
