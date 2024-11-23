import asyncio
import argparse
from crawler import run_crawler


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
