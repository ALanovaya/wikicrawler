import asyncio
from urllib.parse import urlparse
from src.parser import parse_wikipedia_page, is_wikipedia_url
from src.database import create_connection, initialize_database, insert_link, get_links


async def crawl_wikipedia(start_url: str, db_file: str, max_depth: int) -> None:
    """Asynchronously crawl Wikipedia pages and store links in SQLite database."""
    all_links: set[str] = set()

    connection = create_connection(db_file)
    initialize_database(connection)

    async def crawl_page(url: str, depth: int) -> None:
        if depth > max_depth or url in all_links:
            return

        all_links.add(url)
        insert_link(connection, url, depth)

        if depth == max_depth:
            return

        links = await asyncio.to_thread(parse_wikipedia_page, url)

        tasks = []
        for link in links:
            if is_wikipedia_url(link) and link not in all_links:
                task = asyncio.create_task(crawl_page(link, depth + 1))
                tasks.append(task)

        await asyncio.gather(*tasks)

    try:
        await crawl_page(start_url, 1)
        print(
            f"Crawling complete. Found {len(list(get_links(connection)))} unique links."
        )

    finally:
        connection.close()


def validate_url(url: str) -> bool:
    """Validate if the provided URL is a valid Wikipedia article URL."""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)


async def run_crawler(start_url: str, output_file: str, max_depth: int) -> None:
    """Main function to run the Wikipedia crawler."""
    if not validate_url(start_url):
        raise ValueError("Invalid URL provided")

    if not is_wikipedia_url(start_url):
        raise ValueError("The provided URL is not a valid Wikipedia article URL")

    await crawl_wikipedia(start_url, output_file, max_depth)
