from seo_tool.keyword import extract_keywords


def test_extract_keywords():
    text = "SEO tools help analyze SEO and improve SEO."
    result = extract_keywords(text, top_n=2)
    assert result.get('seo') == 3
