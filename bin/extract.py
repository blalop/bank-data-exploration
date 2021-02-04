#!/usr/bin/python3

import argparse
import sqlite3
import os
import sys


try:
    from accountman import extract_directory
except ImportError:
    sys.path.append(os.path.abspath('./'))
    from accountman import extract_directory


def main(dirname, output_format):
    dataframe = extract_directory(dirname)
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
