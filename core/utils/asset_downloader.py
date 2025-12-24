import os
import requests
from urllib.parse import urljoin, urlparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AssetDownloader:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'GOharvest/1.0'})

    def download_asset(self, asset_url):
        try:
            full_url = urljoin(self.base_url, asset_url)
            response = self.session.get(full_url, timeout=10)
            response.raise_for_status()

            # Determine local path
            parsed = urlparse(full_url)
            local_path = self.output_dir / parsed.path.lstrip('/')
            local_path.parent.mkdir(parents=True, exist_ok=True)

            with open(local_path, 'wb') as f:
                f.write(response.content)
            return {
                'url': full_url,
                'local_path': local_path,
                'relative_path': str(local_path.relative_to(self.output_dir)),
            }
        except Exception as e:
            logger.error(f"Failed to download {asset_url}: {e}")
            return None

    def download_assets(self, asset_urls):
        downloaded = []
        for url in asset_urls:
            asset_info = self.download_asset(url)
            if asset_info:
                downloaded.append(asset_info)
        return downloaded
