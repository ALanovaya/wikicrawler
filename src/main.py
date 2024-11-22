import asyncio
from typing import Set
from urllib.parse import urlparse
from parser import parse_wikipedia_page, is_wikipedia_url

MAX_DEPTH = 2
MAX_CONCURRENT_REQUESTS = 10

async def crawl_wikipedia(start_url: str, output_file: str) -> None:
    all_links: Set[str] = set()
    queue = asyncio.Queue()
    queue.put_nowait((start_url, 1))

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async def worker():
        while True:
            url, depth = await queue.get()
            if depth > MAX_DEPTH or url in all_links:
                queue.task_done()
                continue

            all_links.add(url)

            if depth < MAX_DEPTH:
                async with semaphore:
                    links = await asyncio.to_thread(parse_wikipedia_page, url)

                for link in links:
                    if is_wikipedia_url(link) and link not in all_links:
                        queue.put_nowait((link, depth + 1))

            queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(MAX_CONCURRENT_REQUESTS)]
    await queue.join()

    for w in workers:
        w.cancel()

    with open(output_file, 'w') as f:
        for link in sorted(all_links):
            f.write(f"{link}\n")

    print(f"Crawling complete. Found {len(all_links)} unique links.")

def validate_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

async def run_crawler(start_url: str, output_file: str) -> None:
    if not validate_url(start_url):
        raise ValueError("Invalid URL provided")
    
    if not is_wikipedia_url(start_url):
        raise ValueError("The provided URL is not a valid Wikipedia article URL")

    await crawl_wikipedia(start_url, output_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python crawler.py <start_url> <output_file>")
        sys.exit(1)
    
    start_url = sys.argv[1]
    output_file = sys.argv[2]
    
    asyncio.run(run_crawler(start_url, output_file))