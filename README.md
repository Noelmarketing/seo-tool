# SEO Tool

This repository contains a simple command line utility to fetch a web page and
report basic SEO metrics such as title, meta description, heading counts, image
statistics and link information.

## Requirements

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool with a URL to analyze:

```bash
python seo_tool.py https://example.com
```

The tool reports the following metrics:

- Page title and meta description
- Word count
- Heading counts (`h1`-`h6`)
- Image counts, including how many images lack `alt` text
- Canonical URL if present
- Number of internal and external links

## Running Tests

Unit tests use `pytest`. To run them:

```bash
pytest
```
