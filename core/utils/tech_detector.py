import builtwith
import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class TechnologyDetector:
    def __init__(self, url: str, html: str):
        self.url = url
        self.html = html or ''

    def detect(self) -> Dict:
        technologies = {
            'frameworks': self._detect_frameworks(),
            'libraries': self._detect_libraries(),
            'css_frameworks': self._detect_css_frameworks(),
            'analytics': self._detect_analytics(),
            'cms': self._detect_cms(),
            'hosting': self._detect_hosting(),
        }

        try:
            technologies['builtwith'] = builtwith.parse(self.url)
        except Exception as e:
            logger.warning(f"builtwith parse failed for {self.url}: {e}")

        return technologies

    def _detect_frameworks(self) -> List[str]:
        patterns = {
            'React': [r'react', r'__REACT', r'_reactRoot'],
            'Vue': [r'Vue\.', r'__vue__', r'v-if', r'v-for'],
            'Angular': [r'ng-', r'angular', r'ng-version'],
            'Svelte': [r'svelte', r'__svelte'],
            'Next.js': [r'__NEXT_DATA__', r'_next/static'],
            'Nuxt': [r'__NUXT__'],
            'Gatsby': [r'___gatsby'],
        }
        return self._detect_by_patterns(patterns)

    def _detect_libraries(self) -> List[str]:
        patterns = {
            'jQuery': r'jquery',
            'Lodash': r'lodash',
            'Axios': r'axios',
            'Moment.js': r'moment',
            'D3.js': r'd3\.js',
            'Three.js': r'three\.js',
            'GSAP': r'gsap',
        }
        return self._detect_by_patterns(patterns)

    def _detect_css_frameworks(self) -> List[str]:
        patterns = {
            'Bootstrap': r'bootstrap',
            'Tailwind CSS': r'tailwind',
            'Material-UI': r'material-ui|mui',
            'Foundation': r'foundation',
            'Bulma': r'bulma',
        }
        return self._detect_by_patterns(patterns)

    def _detect_analytics(self) -> List[str]:
        patterns = {
            'Google Analytics': r'google-analytics|ga\.js|gtag',
            'Hotjar': r'hotjar',
            'Mixpanel': r'mixpanel',
            'Segment': r'segment',
            'Facebook Pixel': r'facebook.*pixel',
        }
        return self._detect_by_patterns(patterns)

    def _detect_cms(self) -> List[str]:
        patterns = {
            'WordPress': r'wp-content|wordpress',
            'Shopify': r'shopify',
            'Wix': r'wix\.com',
            'Squarespace': r'squarespace',
            'Webflow': r'webflow',
        }
        return self._detect_by_patterns(patterns)

    def _detect_hosting(self) -> List[str]:
        return []

    def _detect_by_patterns(self, patterns: Dict[str, List[str]]) -> List[str]:
        detected = []
        for label, pattern_list in patterns.items():
            if isinstance(pattern_list, str):
                pattern_list = [pattern_list]
            for pattern in pattern_list:
                if re.search(pattern, self.html, re.IGNORECASE):
                    detected.append(label)
                    break
        return list(set(detected))


def detect_technologies(url: str) -> Dict:
    try:
        return builtwith.builtwith(url)
    except Exception as e:
        logger.error(f"Failed to detect technologies for {url}: {e}")
        return {}


def quick_tech_scan(url: str) -> Dict:
    return detect_technologies(url)
