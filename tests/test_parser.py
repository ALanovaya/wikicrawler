import unittest
from unittest.mock import patch
from src.parser import WikipediaParser, parse_wikipedia_page, is_wikipedia_url


class TestWikipediaParser(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        self.parser = WikipediaParser(self.base_url)

    def test_handle_starttag(self):
        self.parser.handle_starttag("a", [("href", "/wiki/Programming_language")])
        self.assertEqual(len(self.parser.links), 1)
        self.assertIn(
            "https://en.wikipedia.org/wiki/Programming_language", self.parser.links
        )

    def test_handle_starttag_invalid_link(self):
        self.parser.handle_starttag("a", [("href", "/wiki/File:Python_logo.png")])
        self.assertEqual(len(self.parser.links), 0)

    def test_handle_starttag_relative_url(self):
        self.parser.handle_starttag("a", [("href", "/wiki/Relative_link")])
        self.assertEqual(len(self.parser.links), 1)
        self.assertIn("https://en.wikipedia.org/wiki/Relative_link", self.parser.links)

    def test_handle_starttag_external_link(self):
        self.parser.handle_starttag("a", [("href", "https://www.python.org")])
        self.assertEqual(len(self.parser.links), 0)

    def test_handle_starttag_anchor_link(self):
        self.parser.handle_starttag("a", [("href", "#section")])
        self.assertEqual(len(self.parser.links), 0)


class TestParserFunctions(unittest.TestCase):
    @patch("src.parser.urllib.request.urlopen")
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

    @patch("src.parser.urllib.request.urlopen")
    def test_parse_wikipedia_page_empty(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = (
            b"<html><body></body></html>"
        )
        links = parse_wikipedia_page("https://en.wikipedia.org/wiki/Empty")
        self.assertEqual(len(links), 0)

    @patch("src.parser.urllib.request.urlopen")
    def test_parse_wikipedia_page_with_links(self, mock_urlopen):
        mock_html = b"""
        <html>
        <body>
            <a href="/wiki/Python">Python</a>
            <a href="/wiki/Java">Java</a>
            <a href="https://www.example.com">External</a>
            <a href="#section">Anchor</a>
        </body>
        </html>
        """
        mock_urlopen.return_value.__enter__.return_value.read.return_value = mock_html
        links = parse_wikipedia_page("https://en.wikipedia.org/wiki/Test")
        self.assertEqual(len(links), 2)
        self.assertIn("https://en.wikipedia.org/wiki/Python", links)
        self.assertIn("https://en.wikipedia.org/wiki/Java", links)

    def test_is_wikipedia_url_valid(self):
        valid_urls = [
            "https://en.wikipedia.org/wiki/Python",
            "https://en.wikipedia.org/wiki/Java_(programming_language)",
            "https://en.wikipedia.org/wiki/C%2B%2B",
        ]
        for url in valid_urls:
            self.assertTrue(is_wikipedia_url(url), f"Failed for URL: {url}")

    @patch("src.parser.urllib.request.urlopen")
    def test_parse_wikipedia_page_invalid_html(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = (
            b"Invalid HTML"
        )
        links = parse_wikipedia_page("https://en.wikipedia.org/wiki/Test")
        self.assertEqual(len(links), 0)

if __name__ == "__main__":
    unittest.main()
