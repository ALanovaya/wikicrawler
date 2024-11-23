from unittest.mock import patch
from src.crawler import run_crawler, validate_url
from unittest import IsolatedAsyncioTestCase, main


class TestCrawler(IsolatedAsyncioTestCase):

    @patch("src.crawler.validate_url")
    @patch("src.crawler.is_wikipedia_url")
    @patch("src.crawler.crawl_wikipedia")
    async def test_run_crawler(self, mock_crawl, mock_is_wiki, mock_validate):
        mock_validate.return_value = True
        mock_is_wiki.return_value = True

        await run_crawler("https://en.wikipedia.org/wiki/Python", "test.db", 2)

        mock_validate.assert_called_once_with("https://en.wikipedia.org/wiki/Python")
        mock_is_wiki.assert_called_once_with("https://en.wikipedia.org/wiki/Python")
        mock_crawl.assert_called_once_with(
            "https://en.wikipedia.org/wiki/Python", "test.db", 2
        )

    def test_validate_url_valid(self):
        self.assertTrue(validate_url("https://en.wikipedia.org/wiki/Python"))

    def test_validate_url_invalid(self):
        self.assertFalse(validate_url("not_a_url"))

    @patch("src.crawler.validate_url")
    @patch("src.crawler.is_wikipedia_url")
    async def test_run_crawler_invalid_url(self, mock_is_wiki, mock_validate):
        mock_validate.return_value = False

        with self.assertRaises(ValueError):
            await run_crawler("invalid_url", "test.db", 2)

    @patch("src.crawler.validate_url")
    @patch("src.crawler.is_wikipedia_url")
    async def test_run_crawler_non_wikipedia_url(self, mock_is_wiki, mock_validate):
        mock_validate.return_value = True
        mock_is_wiki.return_value = False

        with self.assertRaises(ValueError):
            await run_crawler("https://example.com", "test.db", 2)

    @patch("src.crawler.validate_url")
    @patch("src.crawler.is_wikipedia_url")
    @patch("src.crawler.crawl_wikipedia")
    async def test_run_crawler_max_depth(self, mock_crawl, mock_is_wiki, mock_validate):
        mock_validate.return_value = True
        mock_is_wiki.return_value = True

        await run_crawler("https://en.wikipedia.org/wiki/Python", "test.db", 5)

        mock_crawl.assert_called_once_with(
            "https://en.wikipedia.org/wiki/Python", "test.db", 5
        )

    @patch("src.crawler.validate_url")
    @patch("src.crawler.is_wikipedia_url")
    @patch("src.crawler.crawl_wikipedia")
    async def test_run_crawler_different_output_file(
        self, mock_crawl, mock_is_wiki, mock_validate
    ):
        mock_validate.return_value = True
        mock_is_wiki.return_value = True

        await run_crawler("https://en.wikipedia.org/wiki/Python", "custom_output.db", 2)

        mock_crawl.assert_called_once_with(
            "https://en.wikipedia.org/wiki/Python", "custom_output.db", 2
        )

    @patch("src.crawler.validate_url")
    @patch("src.crawler.is_wikipedia_url")
    @patch("src.crawler.crawl_wikipedia")
    async def test_run_crawler_different_start_url(
        self, mock_crawl, mock_is_wiki, mock_validate
    ):
        mock_validate.return_value = True
        mock_is_wiki.return_value = True

        await run_crawler(
            "https://en.wikipedia.org/wiki/Artificial_intelligence", "test.db", 2
        )

        mock_validate.assert_called_once_with(
            "https://en.wikipedia.org/wiki/Artificial_intelligence"
        )
        mock_is_wiki.assert_called_once_with(
            "https://en.wikipedia.org/wiki/Artificial_intelligence"
        )
        mock_crawl.assert_called_once_with(
            "https://en.wikipedia.org/wiki/Artificial_intelligence", "test.db", 2
        )

    @patch("src.crawler.validate_url")
    @patch("src.crawler.is_wikipedia_url")
    @patch("src.crawler.crawl_wikipedia", side_effect=Exception("Crawl error"))
    async def test_run_crawler_crawl_exception(
        self, mock_crawl, mock_is_wiki, mock_validate
    ):
        mock_validate.return_value = True
        mock_is_wiki.return_value = True

        with self.assertRaises(Exception) as context:
            await run_crawler("https://en.wikipedia.org/wiki/Python", "test.db", 2)

        self.assertEqual(str(context.exception), "Crawl error")


if __name__ == "__main__":
    main()
