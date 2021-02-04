
import unittest

import pandas as pd

import accountman.extractor as extr


class TestExtractor(unittest.TestCase):

    def test_report(self):
        report = extr.Report('./test/data/reports/2150-11.pdf')
        self.assertEqual(report.year, 2150)
        self.assertIsNotNone(report.operations)

    def test_extraction(self):
        df_pdf = extr.extract_file('./test/data/reports/2150-11.pdf')
        df_pickle = pd.read_pickle('./test/data/pickles/2150-11.pickle')
        self.assertIsNone(pd.testing.assert_frame_equal(df_pdf, df_pickle))

if __name__ == '__main__':
    unittest.main()
