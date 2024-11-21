import unittest
from unittest.mock import patch
from src.parser import WikipediaParser, parse_wikipedia_page, is_wikipedia_url, get_wikipedia_links

class TestWikipediaParser(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        self.parser = WikipediaParser(self.base_url)

    def test_handle_starttag(self):
        self.parser.handle_starttag('a', [('href', '/wiki/Programming_language')])
        self.assertEqual(len(self.parser.links), 1)
        self.assertIn("https://en.wikipedia.org/wiki/Programming_language", self.parser.links)

    def test_handle_starttag_invalid_link(self):
        self.parser.handle_starttag('a', [('href', '/wiki/File:Python_logo.png')])
        self.assertEqual(len(self.parser.links), 0)

class TestParserFunctions(unittest.TestCase):
    @patch('src.parser.urllib.request.urlopen')
    def test_parse_wikipedia_page(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = b"""
        <html>
            <body>
                <a href="/wiki/Python">Python</a>
                <a href="/wiki/Programming">Programming</a>
                <a href="/wiki/File:Image.jpg">Image</a>
            </body>
        </html>
        """
        links = parse_wikipedia_page("https://en.wikipedia.org/wiki/Test")
        self.assertEqual(len(links), 2)
        self.assertIn("https://en.wikipedia.org/wiki/Python", links)
        self.assertIn("https://en.wikipedia.org/wiki/Programming", links)

    def test_is_wikipedia_url(self):
        self.assertTrue(is_wikipedia_url("https://en.wikipedia.org/wiki/Python"))
        self.assertFalse(is_wikipedia_url("https://www.google.com"))
        self.assertFalse(is_wikipedia_url("https://en.wikipedia.org/w/index.php"))

    @patch('src.parser.parse_wikipedia_page')
    def test_get_wikipedia_links(self, mock_parse):
        mock_parse.return_value = {"https://en.wikipedia.org/wiki/Python", "https://en.wikipedia.org/wiki/Programming"}
        links = get_wikipedia_links("https://en.wikipedia.org/wiki/Test")
        self.assertEqual(len(links), 2)
        self.assertIn("https://en.wikipedia.org/wiki/Python", links)
        self.assertIn("https://en.wikipedia.org/wiki/Programming", links)

    def test_get_wikipedia_links_invalid_url(self):
        with self.assertRaises(ValueError):
            get_wikipedia_links("https://www.google.com")

if __name__ == '__main__':
    unittest.main()