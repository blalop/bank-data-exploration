import unittest
import pandas as pd

import accountman.extractor as extr


class TestExtractor(unittest.TestCase):

    def test_report(self):
        report = extr.Report('./test/data/reports/2150-11.pdf')
        self.assertEqual(report.year, 2150)
        self.assertIsNotNone(report.movements)

    def test_extraction_file(self):
        pdf = extr.extract_file('./test/data/reports/2150-11.pdf')
        pickle = pd.read_pickle('./test/data/pickles/2150-11-movements.pickle')
        self.assertTrue(pdf.equals(pickle))

    def test_extraction_directory(self):
        pdf = extr.extract_directory('./test/data/reports')
        pickle = pd.read_pickle('./test/data/pickles/2150-11-movements.pickle')
        self.assertTrue(pdf.equals(pickle))

if __name__ == '__main__':
    unittest.main()
