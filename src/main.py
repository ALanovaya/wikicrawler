import asyncio
from urllib.parse import urlparse
import argparse
from parser import parse_wikipedia_page, is_wikipedia_url


async def crawl_wikipedia(start_url: str, output_file: str, max_depth: int) -> None:
    all_links: set[str] = set()

    async def crawl_page(url: str, depth: int) -> None:
        if depth > max_depth or url in all_links:
            return

        all_links.add(url)

        if depth == max_depth:
            return

        links = await asyncio.to_thread(parse_wikipedia_page, url)

        tasks = []
        for link in links:
            if is_wikipedia_url(link) and link not in all_links:
                task = asyncio.create_task(crawl_page(link, depth + 1))
                tasks.append(task)

        await asyncio.gather(*tasks)

    await crawl_page(start_url, 1)

    with open(output_file, "w") as f:
        for link in sorted(all_links):
            f.write(f"{link}\n")

    print(f"Crawling complete. Found {len(all_links)} unique links.")


def validate_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)


async def run_crawler(start_url: str, output_file: str, max_depth: int) -> None:
    if not validate_url(start_url):
        raise ValueError("Invalid URL provided")

    if not is_wikipedia_url(start_url):
        raise ValueError("The provided URL is not a valid Wikipedia article URL")

    await crawl_wikipedia(start_url, output_file, max_depth)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl Wikipedia pages.")
    parser.add_argument("start_url", help="The starting Wikipedia URL to crawl.")
    parser.add_argument("output_file", help="The file to write the output links.")
    parser.add_argument(
        "--max_depth", type=int, default=2, help="Maximum depth to crawl (default: 2)."
    )

    args = parser.parse_args()

    start_url = args.start_url
    output_file = args.output_file
    max_depth = args.max_depth

    asyncio.run(run_crawler(start_url, output_file, max_depth))
