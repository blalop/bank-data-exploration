import pandas as pd
import unittest

from accountman.calculator import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator('test/data/reports')
        self.get_pickle = lambda x: f'test/data/pickles/2150-11-{x}.pickle'

    def test_movements(self):
        pickle = pd.read_pickle(self.get_pickle('movements'))
        self.assertTrue(self.calc.movements.equals(pickle))

    def test_salary_movements(self):
        pickle = pd.read_pickle(self.get_pickle('salary'))
        self.assertTrue(self.calc.salary_movements().equals(pickle))

    def test_spending(self):
        pickle = pd.read_pickle(self.get_pickle('spending'))
        self.assertTrue(self.calc.spending().equals(pickle))

    def test_incoming(self):
        pickle = pd.read_pickle(self.get_pickle('incoming'))
        self.assertTrue(self.calc.incoming().equals(pickle))

    def test_speding_by_month(self):
        pickle = pd.read_pickle(self.get_pickle('spending-month'))
        self.assertTrue(self.calc.spending_by_month().equals(pickle))

    def test_incoming_by_month(self):
        pickle = pd.read_pickle(self.get_pickle('incoming-month'))
        self.assertTrue(self.calc.incoming_by_month().equals(pickle))

    def test_combined_by_month(self):
        pickle = pd.read_pickle(self.get_pickle('combined-month'))
        self.assertTrue(self.calc.combined_by_month().equals(pickle))

    def test_diff_by_month(self):
        pickle = pd.read_pickle(self.get_pickle('diff-month'))
        self.assertTrue(self.calc.diff_by_month().equals(pickle))

    def test_spending_by_concept(self):
        pickle = pd.read_pickle(self.get_pickle('spending-concept'))
        self.assertTrue(self.calc.spending_by_concept().equals(pickle))

    def test_incoming_by_concept(self):
        pickle = pd.read_pickle(self.get_pickle('incoming-concept'))
        self.assertTrue(self.calc.incoming_by_concept().equals(pickle))

    def test_spending_abs(self):
        pickle = pd.read_pickle(self.get_pickle('spending-abs'))
        self.assertTrue(self.calc.spending_abs().equals(pickle))

    def test_spending_abs(self):
        pickle = pd.read_pickle(self.get_pickle('spending-biggest'))
        self.assertTrue(self.calc.spending_biggest().equals(pickle))

    def test_combined_by_concept(self):
        pickle = pd.read_pickle(self.get_pickle('combined-concept'))
        self.assertTrue(self.calc.combined_by_concept().equals(pickle))


if __name__ == '__main__':
    unittest.main()
