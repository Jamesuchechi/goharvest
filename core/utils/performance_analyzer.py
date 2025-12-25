from typing import Dict


class PerformanceAnalyzer:
    def __init__(self, url: str, html: str):
        self.url = url
        self.html = html

    def run_lighthouse(self) -> Dict:
        return {
            'lighthouse': {},
            'performance': None,
            'accessibility': None,
            'best_practices': None,
            'seo': None,
            'lcp': None,
            'fid': None,
            'cls': None,
            'tti': None,
            'tbt': None,
            'total_time': 0,
            'dom_content_loaded': None,
            'fcp': None,
            'requests': 0,
            'transfer_size': 0,
            'resource_breakdown': {},
        }
