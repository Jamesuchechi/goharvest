import logging
from pathlib import Path
from typing import Dict, List

import aiohttp
from django.conf import settings

from .safety import assert_public_http_url
from .snapshot import local_path_for

logger = logging.getLogger(__name__)

MAX_ASSET_BYTES = 8 * 1024 * 1024


class AssetDownloader:
    def __init__(self, base_url: str, assets: List[Dict], job_id: str):
        self.base_url = base_url
        self.assets = assets
        self.job_id = job_id
        self.download_dir = Path(settings.MEDIA_ROOT) / 'harvests' / str(job_id)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    async def download(self) -> List[Dict]:
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=8)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            results = []
            for asset in self.assets:
                results.append(await self._download_asset(session, asset))
            return results

    async def _download_asset(self, session: aiohttp.ClientSession, asset: Dict) -> Dict:
        url = asset['url']
        asset_type = asset['type']
        try:
            assert_public_http_url(url)
            async with session.get(url) as response:
                if response.status != 200:
                    return {**asset, 'status': 'failed', 'error': f'HTTP {response.status}'}
                content = await response.read()
                if len(content) > MAX_ASSET_BYTES:
                    return {**asset, 'status': 'failed', 'error': 'asset too large'}
                rel_path = local_path_for(url, asset_type)
                filepath = self.download_dir / rel_path
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_bytes(content)
                return {
                    **asset,
                    'file_path': str(filepath),
                    'rel_path': rel_path,
                    'size': len(content),
                    'status': 'success',
                }
        except Exception as exc:
            logger.error('Failed to download %s: %s', url, exc)
            return {**asset, 'status': 'failed', 'error': str(exc)}
