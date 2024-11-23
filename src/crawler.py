import asyncio
from urllib.parse import urlparse
from src.parser import parse_wikipedia_page, is_wikipedia_url
from src.database import Database


class Crawler:
    def __init__(self, start_url: str, db_file: str, max_depth: int):
        self.start_url = start_url
        self.db = Database(db_file)
        self.max_depth = max_depth

    async def crawl_wikipedia(self) -> None:
        """Asynchronously crawl Wikipedia pages and store links in SQLite database."""
        all_links: set[str] = set()
        self.db.initialize_database()

        async def crawl_page(url: str, depth: int) -> None:
            if depth > self.max_depth or url in all_links:
                return

            all_links.add(url)
            self.db.insert_link(url, depth)

            if depth == self.max_depth:
                return

            links = await asyncio.to_thread(parse_wikipedia_page, url)

            tasks = []
            for link in links:
                if is_wikipedia_url(link) and link not in all_links:
                    task = asyncio.create_task(crawl_page(link, depth + 1))
                    tasks.append(task)

            await asyncio.gather(*tasks)

        try:
            await crawl_page(self.start_url, 1)
            print(
                f"Crawling complete. Found {len(list(self.db.get_links()))} unique links."
            )

        finally:
            self.db.close()

    def validate_url(self, url: str) -> bool:
        """Validate if the provided URL is a valid Wikipedia article URL."""
        parsed_url = urlparse(url)
        return bool(parsed_url.scheme and parsed_url.netloc)

    async def run(self) -> None:
        """Main function to run the Wikipedia crawler."""
        if not self.validate_url(self.start_url):
            raise ValueError("Invalid URL provided")

        if not is_wikipedia_url(self.start_url):
            raise ValueError("The provided URL is not a valid Wikipedia article URL")

        await self.crawl_wikipedia()
