import os
import unittest
import pandas as pd

from src.filtering import filter_by_query, InvalidColumnName


class TestFiltering(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_path = os.path.dirname(os.path.realpath(__file__))
        cls.df = pd.read_csv(os.path.join(current_path, "test_data", "test_data.csv"))

    def test_simple_one_word(self):
        query = "tampere"
        expected = [3, 4, 6, 7]
        self._test_filtering(query, expected)

    def test_simple_regexp(self):
        query = "tam.*re"
        expected = [3, 4, 6, 7]
        self._test_filtering(query, expected)

    def test_filtering_from_one_column(self):
        query = "[Lives] tampere"
        expected = [4, 7]
        self._test_filtering(query, expected)

    def test_or(self):
        query = "[Lives, Born] tampere || [Nationality] finland"
        expected = [2, 3, 4, 6, 7]
        self._test_filtering(query, expected)

    def test_or_different_syntax(self):
        query = "[Lives] [Born] tampere || [Nationality] finland"
        expected = [2, 3, 4, 6, 7]
        self._test_filtering(query, expected)

    def test_and(self):
        query = "[Lives, Born] tampere && [Nationality] finland"
        expected = [3, 4, 6]
        self._test_filtering(query, expected)

    def test_regexp_and(self):
        query = "[Lives] tampere|helsinki && [Nationality] finland"
        expected = [2, 3, 4]
        self._test_filtering(query, expected)

    def test_invalid_column_name_raises_exception(self):
        query = "[Live] tampere"
        with self.assertRaises(InvalidColumnName):
            _ = filter_by_query(self.df, query)

    def _test_filtering(self, query, expected):
        df_filtered = filter_by_query(self.df, query)
        actual = df_filtered.index.to_list()
        self.assertEqual(sorted(actual), sorted(expected))


if __name__ == '__main__':
    unittest.main()
