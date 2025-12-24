import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path

from core.utils.robots_parser import RobotsParser
from core.utils.scraper import WebScraper
from core.utils.tech_detector import detect_technologies


def build_parser():
    parser = argparse.ArgumentParser(description='GOharveST CLI')
    parser.add_argument('--url', required=True, help='Target URL to harvest')
    parser.add_argument(
        '--mode',
        default='content',
        choices=['content', 'media', 'full', 'tech', 'tech-detect'],
        help='Harvest mode',
    )
    parser.add_argument('--depth', type=int, default=1, help='Crawl depth (reserved)')
    parser.add_argument('--output', default='goharvest-output', help='Output directory')
    return parser


def _write_json(path, payload):
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(payload, handle, indent=2)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.mode in ['tech', 'tech-detect']:
        robots = RobotsParser()
        if not robots.can_fetch(args.url):
            print('Robots.txt disallows scraping this URL', file=sys.stderr)
            return 1
        technologies = detect_technologies(args.url)
        _write_json(output_dir / 'technologies.json', technologies)
        print(f"Saved technologies to {output_dir / 'technologies.json'}")
        return 0

    options = {'mode': args.mode, 'depth': args.depth}
    result = asyncio.run(WebScraper().scrape(args.url, options))

    (output_dir / 'index.html').write_text(result.get('html', ''), encoding='utf-8')
    (output_dir / 'content.txt').write_text(result.get('content', ''), encoding='utf-8')
    _write_json(output_dir / 'metadata.json', result.get('metadata', {}))
    _write_json(output_dir / 'assets.json', result.get('assets', []))
    _write_json(output_dir / 'technologies.json', result.get('technologies', {}))

    zip_path = result.get('zip_file')
    if zip_path:
        zip_path = Path(zip_path)
        destination = output_dir / zip_path.name
        shutil.copyfile(zip_path, destination)
        print(f"Saved snapshot to {destination}")

    print(f"Harvest complete. Output in {output_dir}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
