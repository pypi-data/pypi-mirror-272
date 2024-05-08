import unittest
from stopwordz import clean_text

class TestCleanText(unittest.TestCase):
    def test_basic_cleaning(self):
        self.assertEqual(clean_text("Hello, world!"), "hello world")

    def test_with_punctuation(self):
        self.assertEqual(clean_text("Testing, testing, 1 2 3!"), "testing testing 1 2 3")

    def test_with_stopwords(self):
        self.assertEqual(clean_text("This is a test."), "test")

    def test_with_numbers(self):
        self.assertEqual(clean_text("123 testing, testing, 1 2 3!"), "123 testing testing 1 2 3")

if __name__ == '__main__':
    unittest.main()
