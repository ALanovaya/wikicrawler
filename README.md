# Wikipedia Crawler

This project is a Wikipedia crawler that asynchronously crawls Wikipedia pages starting from a given URL, storing the unique links in a SQLite database.

## Description

The Wikipedia Crawler is a Python-based tool that allows you to crawl Wikipedia pages starting from a specified URL. It traverses the links on each page up to a specified depth, storing the discovered links in a SQLite database for further analysis or processing.

## Installation

Installation requires only cloning repository:
```bash
git clone https://github.com/yourusername/wikipedia-crawler.git
cd wikipedia-crawler
```
## Usage

Run the crawler using the following command:
```bash
python -m src.main <start_url> [--database DATABASE] [--max_depth MAX_DEPTH]
```
Arguments:
- `start_url`: The starting Wikipedia URL to crawl (required).
- `--database`: SQLite database path (default: "wikipedia_links.db").
- `--max_depth`: Maximum depth to crawl (default: 2, max: 6).

Example:
```bash
python -m src.main https://en.wikipedia.org/wiki/The_Wall_Street_Journal --max_depth 3 --database example.db
```
This command will start crawling from the Python programming language Wikipedia page, store the results in `example.db`, and crawl up to a depth of 3 links.

## Running Tests

To run the tests, use the following command:
```bash
python -m unittest discover tests
```
## License
Distributed under the MIT License.
See [LICENSE](LICENSE) for more information.
