import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import seo_tool

HTML = """
<html>
<head>
<title>Test Page</title>
<meta name="description" content="This is a test page for SEO metrics" />
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
    assert metrics["internal_links"] == 1
    assert metrics["external_links"] == 1
