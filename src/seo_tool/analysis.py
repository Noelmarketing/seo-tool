from bs4 import BeautifulSoup
from typing import Dict, List


def analyze_html(html: str) -> Dict[str, any]:
    """Extract basic SEO data from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    meta_desc = ''
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta and meta.get('content'):
        meta_desc = meta['content'].strip()
    h1 = ''
    h1_tag = soup.find('h1')
    if h1_tag:
        h1 = h1_tag.get_text(strip=True)
    alt_texts: List[str] = [img.get('alt', '') for img in soup.find_all('img')]
    canonical = ''
    link_tag = soup.find('link', rel='canonical')
    if link_tag and link_tag.get('href'):
        canonical = link_tag['href']
    return {
        'title': title,
        'meta_description': meta_desc,
        'h1': h1,
        'alt_texts': alt_texts,
        'canonical': canonical,
    }
