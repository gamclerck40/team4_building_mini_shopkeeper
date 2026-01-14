import unittest
import pandas as pd
import streamlit as st

from ledger.services import expenditure_statistics_graph

class TestServiceFunctions(unittest.TestCase):
    sample_dictionary = {
            "type": ["지출", "지출", "수입"],
            "category": ["식비", "교통", "급여"],
            "amount": [10000, 5000, 3000000]
        }
    
    def sample_setup(self):
        self.df = pd.DataFrame(self.sample_dictionary)
    
    # 🔹 filter_expenditure
    def test_filter_expenditure(self):
        result = service.filter_expenditure(self.sample_df)

        self.assertTrue((result["type"] == "지출").all())
        self.assertEqual(len(result), 2)

    # 🔹 sum_by_category
    def test_sum_by_category(self):
        df = self.sample_df[self.sample_df["type"] == "지출"]

        result = service.sum_by_category(df)

        expected = pd.DataFrame({
            "category": ["식비", "교통"],
            "amount": [10000, 5000]
        })

        pd.testing.assert_frame_equal(
            result.reset_index(drop=True),
            expected
        )

    # 🔹 expenditure_statistics_graph (조합 함수)
    def test_expenditure_statistics_graph(self):
        result = service.expenditure_statistics_graph(self.sample_df)

        expected = pd.DataFrame({
            "category": ["식비", "교통"],
            "amount": [10000, 5000]
        })

        pd.testing.assert_frame_equal(
            result.reset_index(drop=True),
            expected
        )


if __name__ == "__main__":
    unittest.main()
