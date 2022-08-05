import unittest
from compare_csv import compare_csvs


class TestCompareCSV(unittest.TestCase):
    def test_compare_csvs(self):
        compare_csvs('data/expected.csv', 'data/actual.csv')


if __name__ == '__main__':
    unittest.main()
