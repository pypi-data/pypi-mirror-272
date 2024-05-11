import unittest
from gmailimbox.gmailimbox import GmailBox

class TestGmailBox(unittest.TestCase):
    def test_init(self):
        """Test initialization of GmailBox."""
        gmail = GmailBox()
        self.assertIsNotNone(gmail.service)  # Asserts that the service is setup

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
