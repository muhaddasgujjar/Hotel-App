# tests/test_services/test_auth.py

import unittest
import sys
import os

# Ensure app directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.services.auth import check_credentials

class TestAuth(unittest.TestCase):
    def test_valid_credentials(self):
        self.assertTrue(check_credentials("muhaddas", "1234"))

    def test_invalid_username(self):
        self.assertFalse(check_credentials("wrong", "1234"))

    def test_invalid_password(self):
        self.assertFalse(check_credentials("muhaddas", "wrong"))

    def test_invalid_both(self):
        self.assertFalse(check_credentials("wrong", "wrong"))

if __name__ == '__main__':
    unittest.main()
