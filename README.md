# SEO Tool

A basic SEO analysis tool that crawls a website, collects on‑page data and
produces a CSV report. It demonstrates crawling, basic HTML analysis and keyword
extraction.

## Usage

```bash
pip install -r requirements.txt
python -m seo_tool.cli https://example.com --limit 20 --output report.csv
```

## Structure

- `src/seo_tool/crawler.py` – simple website crawler
- `src/seo_tool/analysis.py` – extract title, meta description, h1, alt texts
- `src/seo_tool/keyword.py` – keyword frequency utility
- `src/seo_tool/report.py` – report generation helpers
- `src/seo_tool/cli.py` – command line interface

## License

MIT
