import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class CrawledPage:
    url: str
    status_code: int
    html: str
    response_time: float


def crawl(base_url: str, limit: int = 50) -> Dict[str, CrawledPage]:
    """Simple crawler that follows internal links up to a limit."""
    visited: Set[str] = set()
    queue: List[str] = [base_url]
    pages: Dict[str, CrawledPage] = {}
    domain = urlparse(base_url).netloc

    while queue and len(visited) < limit:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            resp = requests.get(url, timeout=10)
            response_time = resp.elapsed.total_seconds()
            pages[url] = CrawledPage(
                url=url,
                status_code=resp.status_code,
                html=resp.text,
                response_time=response_time,
            )
            if 'text/html' in resp.headers.get('Content-Type', ''):
                soup = BeautifulSoup(resp.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = urljoin(url, link['href'])
                    parsed = urlparse(href)
                    if parsed.netloc == domain and href not in visited:
                        queue.append(href.split('#')[0])
        except requests.RequestException:
            pages[url] = CrawledPage(url=url, status_code=0, html='', response_time=0.0)
    return pages
