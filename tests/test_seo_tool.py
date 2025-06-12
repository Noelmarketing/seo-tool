import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import seo_tool

HTML = """
<html lang="en">
<head>
<title>Test Page</title>
<meta charset="utf-8" />
<meta name="description" content="This is a test page for SEO metrics" />
<meta name="robots" content="index, follow" />
<meta name="keywords" content="test, seo" />
<meta property="og:title" content="OG Test Title" />
<meta property="og:description" content="OG Description" />
<meta property="og:image" content="/og.jpg" />
<meta name="viewport" content="width=device-width" />
<link rel="canonical" href="https://example.com/test" />
</head>
<body>
<h1>Main Heading</h1>
<h2>Subheading</h2>
<p>Some content here.</p>
<a href="/internal">Internal</a>
<a href="https://external.com">External</a>
<img src="image.jpg" alt="Test image" />
<img src="image2.jpg" />
</body>
</html>
"""


def test_parse_seo_metrics():
    metrics = seo_tool.parse_seo_metrics(HTML, base_url="https://example.com/test")
    assert metrics["title"] == "Test Page"
    assert metrics["meta_description"] == "This is a test page for SEO metrics"
    assert metrics["canonical_url"] == "https://example.com/test"
    assert metrics["word_count"] > 0
    assert metrics["heading_counts"]["h1"] == 1
    assert metrics["heading_counts"]["h2"] == 1
    assert metrics["image_count"] == 2
    assert metrics["images_with_alt"] == 1
    assert metrics["images_without_alt"] == 1
    assert metrics["alt_text_ratio"] == 0.5
    assert metrics["internal_links"] == 1
    assert metrics["external_links"] == 1
    assert metrics["meta_robots"] == "index, follow"
    assert metrics["meta_keywords"] == "test, seo"
    assert metrics["og_title"] == "OG Test Title"
    assert metrics["og_description"] == "OG Description"
    assert metrics["og_image"] == "/og.jpg"
    assert metrics["has_viewport"] is True
    assert metrics["multiple_h1"] is False
    assert isinstance(metrics["reading_ease"], float)
    assert isinstance(metrics["reading_grade"], float)
    assert isinstance(metrics["reading_time"], float)
    assert metrics["html_lang"] == "en"
    assert metrics["charset"] == "utf-8"
    assert metrics["heading_issues"] == []
    assert isinstance(metrics["text_to_html_ratio"], float)
