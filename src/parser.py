import urllib.request
from urllib.parse import urljoin, urlparse
from urllib.error import URLError
from html.parser import HTMLParser


class WikipediaParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return

        href = next((value for attr, value in attrs if attr == "href"), None)
        if not href or not href.startswith("/wiki/") or ":" in href:
            return

        full_url = urljoin(self.base_url, href)
        self.links.add(full_url)


def parse_wikipedia_page(url: str) -> set[str]:
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode("utf-8")
    except URLError as e:
        print(f"Error accessing {url}: {e}")
        return set()

    parser = WikipediaParser(url)
    parser.feed(html)
    return parser.links


def is_wikipedia_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.netloc.endswith("wikipedia.org") and parsed_url.path.startswith(
        "/wiki/"
    )


def get_wikipedia_links(url: str) -> set[str]:
    if not is_wikipedia_url(url):
        raise ValueError("The provided URL is not a valid Wikipedia article URL")
    return parse_wikipedia_page(url)
