import pandas as pd
from typing import Dict
from .crawler import CrawledPage
from .analysis import analyze_html
from .keyword import extract_keywords


def generate_report(pages: Dict[str, CrawledPage]) -> pd.DataFrame:
    rows = []
    for url, page in pages.items():
        if page.html:
            analysis = analyze_html(page.html)
            keywords = extract_keywords(page.html)
            rows.append({
                'url': url,
                'status_code': page.status_code,
                'title': analysis['title'],
                'meta_description': analysis['meta_description'],
                'h1': analysis['h1'],
                'response_time': page.response_time,
                'top_keywords': ', '.join(keywords.keys()),
            })
        else:
            rows.append({
                'url': url,
                'status_code': page.status_code,
                'title': '',
                'meta_description': '',
                'h1': '',
                'response_time': page.response_time,
                'top_keywords': '',
            })
    df = pd.DataFrame(rows)
    return df


def export_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
