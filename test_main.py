import unittest
from main import process_data

class TestProcessData(unittest.TestCase):
    def test_process_data_with_none_input(self):
        """Test that process_data raises ValueError when given None input."""
        with self.assertRaises(ValueError) as context:
            process_data(None)
        
        self.assertEqual(str(context.exception), "Data cannot be None")

if __name__ == '__main__':
    unittest.main()