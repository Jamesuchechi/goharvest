import logging
import os
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests

from .asset_downloader import AssetDownloader
from .robots_parser import RobotsParser
from .tech_detector import detect_technologies

logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, user_agent='GOharvest/1.0 (+https://github.com/Jamesuchechi/goharvest)'):
        self.user_agent = user_agent
        self.robots_parser = RobotsParser(user_agent)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})

    async def scrape(self, url, options=None):
        options = options or {}
        mode = options.get('mode', 'content')  # content, media, full, tech

        if not self.robots_parser.can_fetch(url):
            raise ValueError("Robots.txt disallows scraping this URL")

        technologies = detect_technologies(url)
        if mode in ['tech', 'tech-detect']:
            return {
                'html': '',
                'content': '',
                'metadata': {},
                'assets': [],
                'technologies': technologies,
                'zip_file': None,
            }

        # Scrape content
        html, text, metadata, assets = await self._scrape_content(url, mode)

        # Download assets if needed
        downloaded_assets = []
        zip_path = None
        if mode in ['media', 'full']:
            with tempfile.TemporaryDirectory() as temp_dir:
                downloader = AssetDownloader(url, temp_dir)
                downloaded_assets = downloader.download_assets(assets)
                if mode == 'full':
                    zip_path = self._create_zip(url, html, downloaded_assets)

        return {
            'html': html,
            'content': text,
            'metadata': metadata,
            'assets': assets,
            'technologies': technologies,
            'zip_file': zip_path,
        }

    async def _scrape_content(self, url, mode):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.user_agent,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()

            try:
                await page.goto(url, wait_until='networkidle')
                html = await page.content()
            except Exception as e:
                logger.error(f"Failed to load page {url}: {e}")
                html = ""
            finally:
                await browser.close()

        soup = BeautifulSoup(html, 'html.parser')

        # Extract text
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator='\n', strip=True)

        # Extract metadata
        metadata = self._extract_metadata(soup)

        # Extract assets
        assets = self._extract_assets(soup, url) if mode in ['media', 'full'] else []

        return html, text, metadata, assets

    def _extract_metadata(self, soup):
        metadata = {}
        title = soup.find('title')
        if title:
            metadata['title'] = title.get_text()

        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property')
            content = tag.get('content')
            if name and content:
                metadata[name] = content

        return metadata

    def _extract_assets(self, soup, base_url):
        assets = []

        # CSS
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                assets.append(urljoin(base_url, href))

        # JS
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                assets.append(urljoin(base_url, src))

        # Images
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                assets.append(urljoin(base_url, src))

        # Other assets (fonts, etc.)
        for link in soup.find_all('link', href=True):
            href = link.get('href')
            rel = link.get('rel', [])
            if 'icon' in rel or 'font' in str(rel):
                assets.append(urljoin(base_url, href))

        return list(set(assets))  # Remove duplicates

    def _create_zip(self, url, html, assets):
        domain = urlparse(url).netloc or 'goharvest'
        zip_name = f"{domain}_harvest.zip"
        zip_handle = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        zip_handle.close()
        zip_path = Path(zip_handle.name)

        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('index.html', html)
            for asset in assets:
                local_path = asset['local_path']
                if os.path.exists(local_path):
                    arcname = Path(asset['relative_path']).as_posix()
                    zf.write(local_path, arcname=arcname)

        final_path = zip_path.with_name(zip_name)
        if final_path != zip_path:
            zip_path.replace(final_path)
            zip_path = final_path

        return str(zip_path)
