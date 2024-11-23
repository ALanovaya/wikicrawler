import asyncio
import argparse
from src.crawler import Crawler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl Wikipedia pages.")
    parser.add_argument("start_url", help="The starting Wikipedia URL to crawl.")
    parser.add_argument(
        "--database", default="wikipedia_links.db", help="SQLite database path."
    )
    parser.add_argument(
        "--max_depth", type=int, default=2, help="Maximum depth to crawl (default: 2)."
    )

    args = parser.parse_args()

    start_url = args.start_url
    database = args.database
    max_depth = args.max_depth

    crawler = Crawler(start_url, database, max_depth)
    asyncio.run(crawler.run())
