import os
import unittest
from unittest.mock import patch
import sentry_sdk
from main import main

class TestMain(unittest.TestCase):
    @patch.dict(os.environ, {"TRIGGER_TEST_ERROR": "true"})
    @patch('sentry_sdk.set_context')
    def test_error_triggered(self, mock_set_context):
        """Test that error is triggered and context is set when TRIGGER_TEST_ERROR is true"""
        with self.assertRaises(ZeroDivisionError):
            main()
        
        mock_set_context.assert_called_once_with("error_info", {
            "type": "test_error",
            "purpose": "Sentry integration testing"
        })

    @patch.dict(os.environ, {"TRIGGER_TEST_ERROR": "false"})
    def test_error_not_triggered(self):
        """Test that no error is triggered when TRIGGER_TEST_ERROR is false"""
        # Should complete without error
        main()

if __name__ == '__main__':
    unittest.main()