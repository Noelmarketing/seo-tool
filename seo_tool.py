import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def fetch_html(url: str) -> str:
    """Lädt den HTML-Inhalt einer URL herunter."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_seo_metrics(html: str, base_url: str | None = None) -> dict:
    """Extrahiert SEO-Metriken aus einem HTML-Dokument.

    Args:
        html: Zu analysierender HTML-Inhalt.
        base_url: Optionale Basis-URL der Seite, um Links als intern oder extern einzuordnen.
    """
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_description = meta_tag["content"].strip()

    headings = {f"h{i}": len(soup.find_all(f"h{i}")) for i in range(1, 7)}
    images = soup.find_all("img")
    images_with_alt = sum(1 for img in images if img.get("alt"))
    images_without_alt = len(images) - images_with_alt

    canonical_url = ""
    canonical_tag = soup.find("link", rel="canonical")
    if canonical_tag and canonical_tag.get("href"):
        canonical_url = canonical_tag["href"].strip()

    internal_links = external_links = 0
    links = soup.find_all("a", href=True)
    parsed_base = urlparse(base_url) if base_url else None
    base_domain = parsed_base.netloc if parsed_base else ""
    for link in links:
        href = link["href"].strip()
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
            continue
        if href.startswith("http"):
            domain = urlparse(href).netloc
            if base_domain and domain == base_domain:
                internal_links += 1
            else:
                external_links += 1
        else:
            internal_links += 1

    text = soup.get_text(separator=" ")
    words = [w for w in text.split() if w]

    return {
        "title": title,
        "meta_description": meta_description,
        "word_count": len(words),
        "heading_counts": headings,
        "image_count": len(images),
        "images_with_alt": images_with_alt,
        "images_without_alt": images_without_alt,
        "canonical_url": canonical_url,
        "internal_links": internal_links,
        "external_links": external_links,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Einfacher SEO-Analysator")
    parser.add_argument("url", help="URL, die analysiert werden soll")
    args = parser.parse_args()

    html = fetch_html(args.url)
    metrics = parse_seo_metrics(html, base_url=args.url)

    print(f"Titel: {metrics['title']}")
    print(f"Meta-Description: {metrics['meta_description']}")
    print(f"Wörter insgesamt: {metrics['word_count']}")
    print("Überschriftenanzahl:")
    for heading, count in metrics["heading_counts"].items():
        if count:
            print(f"  {heading}: {count}")
    print(f"Bilder: {metrics['image_count']}")
    print(f"Bilder mit Alt-Text: {metrics['images_with_alt']}")
    print(f"Bilder ohne Alt-Text: {metrics['images_without_alt']}")
    if metrics['canonical_url']:
        print(f"Canonische URL: {metrics['canonical_url']}")
    print(f"Interne Links: {metrics['internal_links']}")
    print(f"Externe Links: {metrics['external_links']}")


if __name__ == "__main__":
    main()
