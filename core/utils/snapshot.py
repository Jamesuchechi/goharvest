import hashlib
import re
import zipfile
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files.base import File


TYPE_DIR = {
    'css': 'css',
    'js': 'js',
    'image': 'assets/images',
    'font': 'assets/fonts',
    'video': 'assets/video',
    'other': 'assets/other',
}


def _safe_name(url: str, asset_type: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name or 'file'
    stem = Path(name).stem[:40] or asset_type
    ext = Path(name).suffix or f'.{asset_type}'
    digest = hashlib.md5(url.encode()).hexdigest()[:8]
    return f'{stem}_{digest}{ext}'


def local_path_for(url: str, asset_type: str) -> str:
    folder = TYPE_DIR.get(asset_type, 'assets/other')
    return f'{folder}/{_safe_name(url, asset_type)}'


def rewrite_html(html: str, url_map: Dict[str, str]) -> str:
    soup = BeautifulSoup(html or '', 'html.parser')
    attr_map = (
        ('img', 'src'),
        ('img', 'data-src'),
        ('script', 'src'),
        ('link', 'href'),
        ('source', 'src'),
        ('video', 'src'),
        ('audio', 'src'),
    )
    for tag, attr in attr_map:
        for node in soup.find_all(tag):
            value = node.get(attr)
            if value and value in url_map:
                node[attr] = url_map[value]
    return str(soup)


def rewrite_css(css_text: str, url_map: Dict[str, str]) -> str:
    def repl(match):
        raw = match.group(1).strip('\'"')
        return f'url({url_map.get(raw, raw)})'

    return re.sub(r'url\(([^)]+)\)', repl, css_text or '')


def build_zip(result, downloaded: List[Dict], rewritten_html: str) -> None:
    job_id = str(result.job_id)
    root = Path(settings.MEDIA_ROOT) / 'harvests' / job_id
    root.mkdir(parents=True, exist_ok=True)
    (root / 'index.html').write_text(rewritten_html or '', encoding='utf-8')

    zip_path = Path(settings.MEDIA_ROOT) / 'harvests' / 'zips'
    zip_path.mkdir(parents=True, exist_ok=True)
    zip_file = zip_path / f'{job_id}.zip'

    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(root / 'index.html', 'index.html')
        for asset in downloaded:
            if asset.get('status') != 'success':
                continue
            rel = asset.get('rel_path')
            src = asset.get('file_path')
            if not rel or not src:
                continue
            path = Path(src)
            if path.exists():
                archive.write(path, rel)

    with zip_file.open('rb') as handle:
        result.zip_file.save(f'{job_id}.zip', File(handle), save=True)
