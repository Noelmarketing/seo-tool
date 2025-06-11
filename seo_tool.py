import argparse
import requests
from bs4 import BeautifulSoup


def fetch_html(url: str) -> str:
    """Fetches HTML content from a URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_seo_metrics(html: str) -> dict:
    """Parses SEO related metrics from an HTML document."""
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_description = meta_tag["content"].strip()

    headings = {f"h{i}": len(soup.find_all(f"h{i}")) for i in range(1, 7)}
    images = soup.find_all("img")
    images_with_alt = sum(1 for img in images if img.get("alt"))

    text = soup.get_text(separator=" ")
    words = [w for w in text.split() if w]

    return {
        "title": title,
        "meta_description": meta_description,
        "word_count": len(words),
        "heading_counts": headings,
        "image_count": len(images),
        "images_with_alt": images_with_alt,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple SEO analyzer")
    parser.add_argument("url", help="URL to analyze")
    args = parser.parse_args()

    html = fetch_html(args.url)
    metrics = parse_seo_metrics(html)

    print(f"Title: {metrics['title']}")
    print(f"Meta description: {metrics['meta_description']}")
    print(f"Word count: {metrics['word_count']}")
    print("Heading counts:")
    for heading, count in metrics["heading_counts"].items():
        if count:
            print(f"  {heading}: {count}")
    print(f"Images: {metrics['image_count']}")
    print(f"Images with alt text: {metrics['images_with_alt']}")


if __name__ == "__main__":
    main()
