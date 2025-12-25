import asyncio
import logging
from typing import Dict, List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from .robots_parser import RobotsParser

logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, url: str, options: Dict):
        self.url = url
        self.options = options or {}
        self.mode = self.options.get('mode', 'full')
        self.depth = self.options.get('depth', 1)
        self.extract_media = self.options.get('extract_media', True)
        self.logger = logging.getLogger(__name__)
        self.robots_parser = RobotsParser()

    async def scrape(self) -> Dict:
        if not self.robots_parser.can_fetch(self.url):
            raise ValueError('Robots.txt disallows scraping this URL')

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=self._get_random_user_agent())
            page = await context.new_page()

            try:
                await page.goto(self.url, wait_until='networkidle')
                await page.wait_for_load_state('domcontentloaded')
                await asyncio.sleep(2)
                html = await page.content()
            finally:
                await browser.close()

        soup = BeautifulSoup(html, 'html.parser')
        content = self._extract_text(soup)
        structured_data = self._extract_structured(soup)
        metadata = self._extract_metadata(soup)
        links = self._extract_links(soup)
        assets = self._extract_assets(soup) if self.extract_media else []

        return {
            'html': html,
            'content': content,
            'structured': structured_data,
            'metadata': metadata,
            'links': links,
            'assets': assets,
        }

    def _extract_text(self, soup: BeautifulSoup) -> str:
        for element in soup(['script', 'style', 'meta', 'link']):
            element.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        return '\n'.join(line for line in lines if line)

    def _extract_structured(self, soup: BeautifulSoup) -> Dict:
        return {
            'headings': {
                f'h{i}': [h.get_text().strip() for h in soup.find_all(f'h{i}')]
                for i in range(1, 7)
            },
            'lists': [ul.get_text().strip() for ul in soup.find_all(['ul', 'ol'])],
            'tables': self._extract_tables(soup),
        }

    def _extract_tables(self, soup: BeautifulSoup) -> List[List[str]]:
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for row in table.find_all('tr'):
                rows.append([cell.get_text().strip() for cell in row.find_all(['th', 'td'])])
            tables.append(rows)
        return tables

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        metadata = {}

        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content

        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()

        return metadata

    def _extract_links(self, soup: BeautifulSoup) -> Dict:
        base_domain = urlparse(self.url).netloc
        internal = []
        external = []

        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            parsed = urlparse(href)

            if parsed.netloc == base_domain or not parsed.netloc:
                internal.append(href)
            else:
                external.append(href)

        return {
            'internal': list(set(internal)),
            'external': list(set(external)),
        }

    def _extract_assets(self, soup: BeautifulSoup) -> List[Dict]:
        assets = []

        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                assets.append({
                    'type': 'image',
                    'url': self._resolve_url(src),
                    'alt': img.get('alt', ''),
                })

        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                assets.append({
                    'type': 'css',
                    'url': self._resolve_url(href),
                })

        for script in soup.find_all('script', src=True):
            assets.append({
                'type': 'js',
                'url': self._resolve_url(script['src']),
            })

        return assets

    def _resolve_url(self, url: str) -> str:
        return urljoin(self.url, url)

    def _get_random_user_agent(self) -> str:
        from fake_useragent import UserAgent

        ua = UserAgent()
        return ua.random
