import pytest

from core.utils.scraper import WebScraper


@pytest.mark.skip(reason='Requires Playwright and network access.')
@pytest.mark.asyncio
async def test_scraper_extracts_content():
    scraper = WebScraper('https://example.com', {'mode': 'full'})
    result = await scraper.scrape()
    assert 'html' in result
    assert 'content' in result
