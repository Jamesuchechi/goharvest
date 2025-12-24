import builtwith
import logging

logger = logging.getLogger(__name__)


def detect_technologies(url):
    try:
        tech = builtwith.builtwith(url)
        return tech
    except Exception as e:
        logger.error(f"Failed to detect technologies for {url}: {e}")
        return {}