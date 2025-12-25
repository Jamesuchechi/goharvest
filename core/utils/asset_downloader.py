import asyncio
import logging
from pathlib import Path
from typing import Dict, List

import aiohttp

logger = logging.getLogger(__name__)


class AssetDownloader:
    def __init__(self, base_url: str, assets: List[Dict]):
        self.base_url = base_url
        self.assets = assets
        self.download_dir = Path('media/harvests/assets')
        self.download_dir.mkdir(parents=True, exist_ok=True)

    async def download(self) -> List[Dict]:
        tasks = [self._download_asset(asset) for asset in self.assets]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, dict)]

    async def _download_asset(self, asset: Dict) -> Dict:
        url = asset['url']
        asset_type = asset['type']

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.read()
                        filename = self._generate_filename(url, asset_type)
                        filepath = self.download_dir / filename
                        filepath.parent.mkdir(parents=True, exist_ok=True)
                        with open(filepath, 'wb') as handle:
                            handle.write(content)
                        return {
                            **asset,
                            'file_path': str(filepath),
                            'size': len(content),
                            'status': 'success',
                        }
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return {
                **asset,
                'status': 'failed',
                'error': str(e),
            }

    def _generate_filename(self, url: str, asset_type: str) -> str:
        from urllib.parse import urlparse
        import hashlib

        parsed = urlparse(url)
        path = parsed.path
        hash_obj = hashlib.md5(url.encode())
        hash_str = hash_obj.hexdigest()[:8]
        ext = Path(path).suffix or f'.{asset_type}'
        return f"{asset_type}_{hash_str}{ext}"
