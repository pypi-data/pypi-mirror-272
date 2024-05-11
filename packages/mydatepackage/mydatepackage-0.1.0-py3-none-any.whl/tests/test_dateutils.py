import unittest
from mydatepackage.dateutils import get_current_date, add_days_to_date

class TestDateUtils(unittest.TestCase):
    def test_add_days_to_date(self):
        self.assertEqual(add_days_to_date("2023-01-01", 10), "2023-01-11")

if __name__ == '__main__':
    unittest.main()