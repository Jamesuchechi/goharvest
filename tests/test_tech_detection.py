from core.utils.tech_detector import TechnologyDetector


def test_detect_frameworks_from_html():
    html = """
    <html>
      <head>
        <script>window.__NEXT_DATA__ = {};</script>
      </head>
      <body>
        <div id="root"></div>
      </body>
    </html>
    """
    detector = TechnologyDetector('https://example.com', html)
    tech = detector.detect()
    assert 'frameworks' in tech
    assert 'Next.js' in tech['frameworks']
