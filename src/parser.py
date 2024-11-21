import urllib.request
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
from typing import Set, List

class WikipediaParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: Set[str] = set()

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    if value and value.startswith('/wiki/') and ':' not in value:
                        full_url = urljoin(self.base_url, value)
                        self.links.add(full_url)

def parse_wikipedia_page(url: str) -> Set[str]:
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        
        parser = WikipediaParser(url)
        parser.feed(html)
        return parser.links
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return set()

def is_wikipedia_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.netloc.endswith('wikipedia.org') and parsed_url.path.startswith('/wiki/')

def get_wikipedia_links(url: str) -> Set[str]:
    if not is_wikipedia_url(url):
        raise ValueError("The provided URL is not a valid Wikipedia article URL")
    return parse_wikipedia_page(url)