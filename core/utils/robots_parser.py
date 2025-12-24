import requests
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import logging

logger = logging.getLogger(__name__)


class RobotsParser:
    def __init__(self, user_agent='GOharvest/1.0'):
        self.user_agent = user_agent
        self.parsers = {}  # Cache parsers by domain

    def can_fetch(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain not in self.parsers:
            self.parsers[domain] = self._load_robots(parsed)
        return self.parsers[domain].can_fetch(self.user_agent, url)

    def _load_robots(self, parsed_url):
        rp = RobotFileParser()
        scheme = parsed_url.scheme or 'http'
        robots_url = urljoin(f'{scheme}://{parsed_url.netloc}', '/robots.txt')
        try:
            rp.set_url(robots_url)
            rp.read()
            logger.info(f"Loaded robots.txt for {parsed_url.netloc}")
        except Exception as e:
            logger.warning(f"Failed to load robots.txt for {parsed_url.netloc}: {e}")
        return rp
