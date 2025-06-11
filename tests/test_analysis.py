from seo_tool.analysis import analyze_html


HTML = """
<html>
  <head>
    <title>Example</title>
    <meta name='description' content='Test page'>
    <link rel='canonical' href='https://example.com' />
  </head>
  <body>
    <h1>Heading</h1>
    <img src='a.jpg' alt='alt text'>
  </body>
</html>
"""


def test_analyze_html():
    data = analyze_html(HTML)
    assert data['title'] == 'Example'
    assert data['meta_description'] == 'Test page'
    assert data['h1'] == 'Heading'
    assert data['canonical'] == 'https://example.com'
    assert 'alt text' in data['alt_texts']
