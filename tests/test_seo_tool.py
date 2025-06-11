import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import seo_tool

HTML = """
<html>
<head>
<title>Test Page</title>
<meta name="description" content="This is a test page for SEO metrics" />
</head>
<body>
<h1>Main Heading</h1>
<h2>Subheading</h2>
<p>Some content here.</p>
<img src="image.jpg" alt="Test image" />
</body>
</html>
"""


def test_parse_seo_metrics():
    metrics = seo_tool.parse_seo_metrics(HTML)
    assert metrics["title"] == "Test Page"
    assert metrics["meta_description"] == "This is a test page for SEO metrics"
    assert metrics["word_count"] > 0
    assert metrics["heading_counts"]["h1"] == 1
    assert metrics["heading_counts"]["h2"] == 1
    assert metrics["image_count"] == 1
    assert metrics["images_with_alt"] == 1
