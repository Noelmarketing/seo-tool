import argparse
import json
import re
from urllib.parse import urlparse

__version__ = "1.3.0"

import requests
from bs4 import BeautifulSoup
from textstat import flesch_reading_ease, flesch_kincaid_grade


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

    html_lang = ""
    if soup.html and soup.html.get("lang"):
        html_lang = soup.html["lang"].strip()

    charset = ""
    charset_tag = soup.find("meta", charset=True)
    if charset_tag:
        charset = charset_tag.get("charset", "").lower().strip()
    else:
        ct_tag = soup.find("meta", attrs={"http-equiv": "Content-Type"})
        if ct_tag and ct_tag.get("content"):
            m = re.search(r"charset=([\w-]+)", ct_tag["content"], re.I)
            if m:
                charset = m.group(1).lower()

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_description = meta_tag["content"].strip()

    headings = {f"h{i}": len(soup.find_all(f"h{i}")) for i in range(1, 7)}
    multiple_h1 = headings.get("h1", 0) > 1

    heading_issues: list[str] = []
    all_headings = soup.find_all(re.compile(r"^h[1-6]$"))
    last_level = 0
    seen_h1 = False
    for tag in all_headings:
        level = int(tag.name[1])
        if not seen_h1 and level != 1:
            heading_issues.append("Erste Überschrift ist nicht h1")
        if last_level and level > last_level + 1:
            heading_issues.append(f"Sprung von h{last_level} zu h{level}")
        if level == 1:
            seen_h1 = True
        last_level = level
    if not seen_h1:
        heading_issues.append("Keine h1-Überschrift gefunden")
    images = soup.find_all("img")
    images_with_alt = sum(1 for img in images if img.get("alt"))
    images_without_alt = len(images) - images_with_alt

    robots = ""
    robots_tag = soup.find("meta", attrs={"name": "robots"})
    if robots_tag and robots_tag.get("content"):
        robots = robots_tag["content"].strip()

    keywords = ""
    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    if keywords_tag and keywords_tag.get("content"):
        keywords = keywords_tag["content"].strip()

    og_title = ""
    og_title_tag = soup.find("meta", property="og:title")
    if og_title_tag and og_title_tag.get("content"):
        og_title = og_title_tag["content"].strip()

    og_description = ""
    og_desc_tag = soup.find("meta", property="og:description")
    if og_desc_tag and og_desc_tag.get("content"):
        og_description = og_desc_tag["content"].strip()

    og_image = ""
    og_img_tag = soup.find("meta", property="og:image")
    if og_img_tag and og_img_tag.get("content"):
        og_image = og_img_tag["content"].strip()

    canonical_url = ""
    canonical_tag = soup.find("link", rel="canonical")
    if canonical_tag and canonical_tag.get("href"):
        canonical_url = canonical_tag["href"].strip()

    has_viewport = bool(soup.find("meta", attrs={"name": "viewport"}))

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
    reading_ease = flesch_reading_ease(text)
    reading_grade = flesch_kincaid_grade(text)
    reading_time = len(words) / 200
    text_to_html_ratio = len(text) / len(html) if html else 0
    alt_text_ratio = images_with_alt / len(images) if images else 0

    return {
        "title": title,
        "meta_description": meta_description,
        "word_count": len(words),
        "heading_counts": headings,
        "image_count": len(images),
        "images_with_alt": images_with_alt,
        "images_without_alt": images_without_alt,
        "alt_text_ratio": alt_text_ratio,
        "html_lang": html_lang,
        "charset": charset,
        "heading_issues": heading_issues,
        "text_to_html_ratio": text_to_html_ratio,
        "canonical_url": canonical_url,
        "meta_robots": robots,
        "meta_keywords": keywords,
        "og_title": og_title,
        "og_description": og_description,
        "og_image": og_image,
        "internal_links": internal_links,
        "external_links": external_links,
        "reading_ease": reading_ease,
        "reading_grade": reading_grade,
        "reading_time": reading_time,
        "has_viewport": has_viewport,
        "multiple_h1": multiple_h1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Einfacher SEO-Analysator")
    parser.add_argument("url", help="URL, die analysiert werden soll")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    args = parser.parse_args()

    html = fetch_html(args.url)
    metrics = parse_seo_metrics(html, base_url=args.url)

    if args.json:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
        return

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
    print(f"Alt-Text-Quote: {metrics['alt_text_ratio']:.2f}")
    if metrics['html_lang']:
        print(f"Sprache der Seite: {metrics['html_lang']}")
    if metrics['charset']:
        print(f"Zeichenkodierung: {metrics['charset']}")
    if metrics['heading_issues']:
        for issue in metrics['heading_issues']:
            print(f"Warnung: {issue}")
    print(f"Text-zu-HTML-Verhältnis: {metrics['text_to_html_ratio']:.2f}")
    if metrics['canonical_url']:
        print(f"Canonische URL: {metrics['canonical_url']}")
    if metrics['meta_robots']:
        print(f"Meta-Robots: {metrics['meta_robots']}")
    if metrics['meta_keywords']:
        print(f"Meta-Keywords: {metrics['meta_keywords']}")
    if metrics['og_title']:
        print(f"OG Title: {metrics['og_title']}")
    if metrics['og_description']:
        print(f"OG Description: {metrics['og_description']}")
    if metrics['og_image']:
        print(f"OG Image: {metrics['og_image']}")
    print(f"Interne Links: {metrics['internal_links']}")
    print(f"Externe Links: {metrics['external_links']}")
    print(f"Lesbarkeitsindex: {metrics['reading_ease']:.2f}")
    print(f"Lesestufe (Flesch-Kincaid): {metrics['reading_grade']:.2f}")
    print(f"Geschätzte Lesezeit: {metrics['reading_time']:.2f} Minuten")
    print(f"Viewport-Tag vorhanden: {metrics['has_viewport']}")
    if metrics['multiple_h1']:
        print("Warnung: Mehrere H1-Überschriften gefunden")


if __name__ == "__main__":
    main()
