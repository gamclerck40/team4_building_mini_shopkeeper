import unittest
import pandas as pd

from ledger import services


class TestServicesModule(unittest.TestCase):
    """
    services.py 전체를 하나의 서비스 모듈로 보고 테스트
    """

    sample_dict = {
            "type": ["지출", "지출", "수입"],
            "category": ["식비", "교통", "급여"],
            "amount": [10000, 5000, 3000000]
        }
    def setUp(self):
        self.sample_df = pd.DataFrame(self.sample_dict)


    def test_normal_expenditure_statistics(self):
        df = pd.DataFrame({
            "type": ["지출", "지출", "수입"],
            "category": ["식비", "교통", "급여"],
            "amount": [10000, 5000, 3000000]
        })

        result = services.expenditure_statistics_graph(df)

        expected = pd.DataFrame({
            "category": ["식비", "교통"],
            "amount": [10000, 5000]
        })

        pd.testing.assert_frame_equal(
            result.reset_index(drop=True),
            expected
        )

    def test_no_expenditure_returns_empty_dataframe(self):
        df = pd.DataFrame({
            "type": ["수입"],
            "category": ["급여"],
            "amount": [3000000]
        })

        result = services.expenditure_statistics_graph(df)

        expected = pd.DataFrame(columns=["category", "amount"])
        pd.testing.assert_frame_equal(result, expected)

    def test_calculate_summary_only_income(self):
        df = pd.DataFrame({
            "type":["수입"], "amount":[1000000]
        })
        self.assertEqual(services.calculate_summary(df),{"income":1000000,
                                                         "expense":0,
                                                         "balance":1000000})
    
    def test_calculate_summary_only_expense(self):
        df = pd.DataFrame({
            "type":["지출"],"amount":[500000]
        })
        self.assertEqual(services.calculate_summary(df),{"income":0,
                                                         "expense":500000,
                                                         "balance":-500000})

    


if __name__ == "__main__":
    unittest.main()