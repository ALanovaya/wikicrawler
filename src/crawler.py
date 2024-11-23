import asyncio
from urllib.parse import urlparse
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
