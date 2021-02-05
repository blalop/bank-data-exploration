import unittest

from accountman.calculator import Calculator
from accountman.plotter import plot


class TestPlotter(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator('test/data/reports')

    def test_plotter(self):
       self.assertIsNotNone(plot(self.calc))

if __name__ == '__main__':
    unittest.main()
