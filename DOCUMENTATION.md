
GOharveST Documentation
Table of Contents

    Overview
    Installation
    Configuration
    Usage Guide
        Web Interface
        CLI Mode
        API Endpoints
    Features in Detail
    Troubleshooting
    Development
    Ethics and Legal
    FAQ

Overview

GOharveST is a Python-based platform for ethical web scraping focused on frontend intelligence. It extracts public content, detects technologies, and reconstructs site structures. This doc covers setup, usage, and advanced topics.
Installation
Prerequisites

    Python 3.10+
    Redis (for caching and queues)
    Browser (for automation: Chrome/Firefox via Playwright/Selenium)
    Git

Step-by-Step

    Clone: git clone https://github.com/Jamesuchechi/goharvest.git
    Virtual Env: python -m venv venv && source venv/bin/activate
    Dependencies: pip install -r requirements.txt
    Env Setup: Create .env with keys (see README).
    Migrations: python manage.py migrate
    Run: python manage.py runserver
    Celery/Redis: Run in background.

Docker

    docker-compose build
    docker-compose up -d
    Access at http://localhost:8000

Configuration

    .env Variables:
        DJANGO_SECRET_KEY: Secure random string.
        REDIS_URL: Redis connection string.
        ALLOWED_HOSTS: Comma-separated hosts (e.g., * for dev).
        PROXY_LIST: Optional proxies for evasion (e.g., http://proxy1:port,http://proxy2:port).
        USER_AGENTS: Path to user agents file or use fake-useragent.
        RATE_LIMIT: Requests per minute (default: 60).
        AI_MODEL: Optional Hugging Face model for AI features.
    Settings.py: Customize Django settings for production (e.g., static files, logging).

Usage Guide
Web Interface

    Navigate to /harvest/ endpoint.
    Input URL and options:
        Modes: Content, Media, Full Snapshot, Tech Detect Only.
        Depth: Single page or crawl (levels 1-3).
        Async: Enable for background processing.
    Monitor via dashboard (WebSockets for live updates).
    Download ZIP/JSON.

CLI Mode

(If implemented in cli.py):

    python cli.py --help for options.
    Example: python cli.py --url https://example.com --mode full --depth 2 --output ./output --proxy http://proxy:port

API Endpoints

Using Django REST Framework:

    POST /api/harvest/: Submit job. Body: { "url": "https://example.com", "mode": "full", "options": {"depth": 2} }. Returns job ID.
    GET /api/jobs/<id>/: Check status and results.
    GET /api/tech-detect/: Quick tech scan without full harvest.
    Auth: API keys via headers (implement TokenAuthentication).

Features in Detail
Frontend Harvesting

    Uses BeautifulSoup for HTML/CSS parsing.
    JS beautification via js-beautify.
    Asset reconstruction: Downloads and organizes into folders.

Content Extraction

    Structured parsing: Headings (h1-h6), paragraphs, tables (pandas for export).
    Meta: OpenGraph, Twitter Cards.

Media Scraping

    Images: Via selectors and CSS backgrounds.
    Videos: Embed codes only (no downloads if copyrighted).

Technology Detection

    Libraries: builtwith for comprehensive scans.
    Custom rules for frameworks (e.g., React via hooks detection).

Dynamic Support

    Playwright preferred for headless browsing.
    Handles SPAs by waiting for DOM stability.

Enhancements

    Scrapy: Custom spiders for multi-page.
    Async: aiohttp for concurrent requests.
    Caching: Redis stores fetched pages.
    Rate Limiting: Per-domain throttling.
    User Agents/Proxies: Rotation to prevent bans.
    Exports: ZIP (default), JSON, Markdown reports.
    Performance Reports: Integrate Lighthouse for metrics.
    AI: LLM summaries of code (e.g., "This JS file uses React hooks for state management").
    Component Detection: Parse for class patterns (e.g., Tailwind utilities).
    Crawling: Breadth-first with depth limit.
    Batch: Process URL lists from file/API.
    Visuals: Generate DOM trees as images (via Graphviz).
    Diff: Compare two harvests for changes.

Troubleshooting

    Blocked by Site: Use proxies, slower rates, or check robots.txt.
    Redis Errors: Ensure Redis is running; check connections.
    Browser Issues: Update drivers; try Selenium if Playwright fails.
    Memory High: Limit depth; use headless mode.
    Logs: Check DEBUG=True output or Celery logs.

Development

    Testing: Use pytest: pytest tests/.
    Linting: Black & Flake8: black . && flake8.
    CI/CD: GitHub Actions workflow for builds/tests.
    Extending: Add custom extractors via plugins (e.g., subclass Scrapy spiders).
    Edge Cases: Test with JS-heavy sites (e.g., React apps), international chars.

Ethics and Legal

    Comply with ToS: Log all actions; add user consent prompts.
    Laws: Reference GDPR (EU), CCPA (CA), DMCA (US).
    Best Practices: Cite EFF guidelines on scraping.
    Disclaimer: Not for commercial scraping without permission.

FAQ

    Is it legal? Depends on use; public data is often fair, but check ToS.
    Handles Anti-Scraping? Partially via evasion, but not foolproof.
    Custom Exports? Yes, extend via API.
    Support for Other Languages? Planned; currently English-focused.
    Contributions? See CONTRIBUTING.md.

For questions, open an issue on GitHub.

Last Updated: December 24, 2025
Author: Okpara James Uchechi
