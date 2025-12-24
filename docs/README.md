🌾 GOharveST: Public Web Content & Frontend Code Intelligence Platform

GitHub license
GitHub stars
GitHub issues
GitHub forks
Python Version

GOharveST is an open-source web scraping and frontend intelligence platform designed to extract publicly available web content, media assets, and frontend source code from any given URL. It transforms websites into structured, downloadable project snapshots, focusing on the "how" behind the frontend—revealing structures, technologies, and assets without touching backend or private data.

Unlike basic scrapers that grab only text, GOharveST provides a developer-centric view, ideal for learning, auditing, and inspiration. It emphasizes ethical scraping, respecting robots.txt, rate limits, and public access only.
🚀 Key Features
🧱 Frontend Source Code Harvesting

    Extracts and organizes HTML structure.
    Pulls linked and inline CSS.
    Downloads and beautifies JavaScript files.
    Reconstructs asset folders for a ready-to-run local snapshot.

Example output structure:
text

goharvest-output/
├── index.html
├── css/
│   └── main.css
├── js/
│   └── app.js
├── assets/
│   ├── images/
│   │   └── logo.png
│   └── fonts/
│       └── font.woff

📄 Content Extraction

    Captures page text, headings, and structured elements (e.g., lists, tables).
    Collects meta tags for SEO insights.
    Identifies internal/external links and sections like blogs or docs.

🖼️ Media Scraping

    Downloads images in original resolution, including CSS backgrounds.
    Handles embedded videos (HTML5 or public embeds like YouTube).
    Extracts icons, fonts, and other static assets.

🧠 Technology Detection

    Automatically identifies:
        Frontend frameworks (e.g., React, Vue, Angular, Svelte).
        CSS libraries (e.g., Bootstrap, Tailwind CSS, Material-UI).
        JavaScript tools (e.g., jQuery, Lodash, Axios).
        Build systems and analytics (e.g., Webpack, Vite, Google Analytics, Hotjar).

⚙️ Dynamic Page Support

    Leverages browser automation for:
        JavaScript-rendered content.
        Infinite scrolling and lazy-loading.
        Single Page Applications (SPAs).
    Supports headless mode for efficiency.

Additional Enhancements

    Integrates Scrapy for robust crawling with spiders and middleware for anti-bot evasion.
    Uses async libraries (e.g., aiohttp) for faster fetches.
    Implements caching with Redis for repeated scans.
    Adds rate limiting to mimic human behavior and avoid blocks.
    Rotates user agents and supports proxies for better evasion.
    Honors robots.txt with built-in parsing.
    Supports more export formats: JSON for data, Markdown for reports, or static site previews.
    Generates site performance reports (e.g., asset sizes, load times via Lighthouse integration).
    AI-powered code explanations (using LLMs for summaries).
    Component detection for reusable UI elements.
    Full-site crawling with depth controls.
    Batch processing for multiple URLs.
    Visual DOM maps and asset visualizations.
    Diff mode for comparing harvests over time.

❗ Scope, Ethics, & Limitations

GOharveST is strictly limited to publicly accessible frontend resources. It respects web standards and ethics by:

    Honoring robots.txt files to avoid disallowed paths.
    Using polite crawling with rate limiting and user-agent identification.
    Never accessing authenticated areas, paywalled content, or server-side data.

It does not:

    Bypass security (e.g., no credential stuffing or exploits).
    Extract backend code, databases, or API logic.
    Handle non-public network requests.

Important: Always check website terms of service (ToS) and local laws (e.g., GDPR, DMCA) before use. GOharveST is for educational/research purposes—misuse could violate copyrights or anti-scraping policies.
🧩 Why Use GOharveST?

Traditional scrapers focus on data extraction; GOharveST emphasizes frontend forensics:

    How is the site built? Unpack code organization and best practices.
    What powers it? Detect stacks for competitive analysis.
    Inspiration & Learning: Reverse-engineer UIs for education or replication.

Use cases:

    Frontend developers studying real-world implementations.
    Auditors checking for vulnerabilities or compliance.
    Designers gathering UI/UX patterns.
    Researchers analyzing web trends.

🛠️ Tech Stack

    Backend: Django (core framework), Django REST Framework (API), Celery (async tasks), Redis (queuing & caching).
    Scraping Engine: BeautifulSoup (static HTML), Selenium/Playwright (dynamic rendering), Requests/HTTPX (HTTP handling), Scrapy (crawling spiders).
    Frontend: React (dashboard for progress tracking), with fallback to Django Templates.
    Other: ZIP for exports, Docker for deployment, libraries like builtwith or wappalyzer-python for tech detection, fake-useragent for rotation, ratelimit for throttling, tqdm for progress bars, WebSockets for real-time updates.
    Language: Python 3.10+ (Note: "goharvest" is thematic for "go harvest the web"; the project is Python-based).
    AI Integration: Optional Hugging Face models for content analysis or code explanations.

📦 Installation

    Clone the repo:
    text

git clone https://github.com/Jamesuchechi/goharvest.git
cd goharvest

Set up a virtual environment:
text

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
text

pip install -r requirements.txt

(Dependencies include: django, djangorestframework, celery, redis, beautifulsoup4, selenium, playwright, requests, httpx, scrapy, aiohttp, builtwith, fake-useragent, ratelimit, tqdm, etc.)
Configure environment variables (create a `.env` file):
text

DJANGO_SECRET_KEY=your_secret_key_here
REDIS_URL=redis://localhost:6379/0
DEBUG=True  # Set to False in production

Install browser drivers (for Selenium/Playwright):

    For Playwright: playwright install

Run database migrations:
text

python manage.py migrate

Start the development server:
text

    python manage.py runserver

    For background tasks: In separate terminals:
        Start Redis (if not running): redis-server
        Start Celery: celery -A goharvest worker -l info

Docker Alternative:

    Build and run: docker-compose up -d
    (Ensure Dockerfile and docker-compose.yml are in the repo.)

🧪 Quick Start

    Access the web interface at http://localhost:8000.
    Browse recent jobs on the dashboard.
    Create harvests via the API or CLI.

CLI:

    python -m cli.main --url https://example.com --mode full --output ./snapshot

API:

    POST /api/harvest/ with body: { "url": "https://example.com", "options": { "mode": "full", "depth": 1 } }
    GET /api/jobs/<id>/ for status
    GET /api/jobs/<id>/result/ for the result payload
    GET /api/tech-detect/?url=https://example.com
🗺️ Roadmap

    Short-term: AI explanations, component detection.
    Medium-term: Full-site crawling, visual maps.
    Long-term: GitHub exports, plugin system, multi-language support.

🤝 Contributing

Fork, branch, PR! See CONTRIBUTING.md for details. Follow CODE_OF_CONDUCT.md.
📜 License

MIT License.
👤 Author

Okpara James Uchechi
GitHub | LinkedIn | Email



goharvest/
├── goharvest/                  # Main Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py              # Celery app configuration
│
├── core/                       # Core app: models, utilities, task logic
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # HarvestJob, HarvestResult, etc.
│   ├── tasks.py                # Celery tasks (scraping logic)
│   ├── utils/
│   │   ├── scraper.py          # Main scraping engine (Playwright/Scrapy)
│   │   ├── tech_detector.py    # Technology detection logic
│   │   ├── asset_downloader.py
│   │   └── robots_parser.py    # robots.txt compliance
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│
├── api/                        # Django REST Framework endpoints
│   ├── __init__.py
│   ├── serializers.py
│   ├── viewsets.py
│   ├── urls.py
│   └── tests/
│
├── dashboard/                  # Frontend app (React or Django templates)
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   │   ├── dashboard/
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   │   ├── job_list.html
│   │   │   └── job_detail.html
│   └── (If using React: see below)
│
├── frontend/                   # Optional: Separate React/Vite frontend (recommended for rich UI)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/api.js     # API calls to Django backend
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── cli/                        # Command-line interface tools
│   ├── __init__.py
│   ├── main.py                 # Entry point: python -m cli.main
│   └── commands/
│       └── harvest.py          # goharvest harvest --url ...
│
├── media/                      # User-uploaded or temporary files (gitignore)
│   └── harvests/               # Downloaded assets, ZIPs (not committed)
│
├── static/                     # Global static files (CSS, JS, images)
│   ├── admin/
│   └── site/
│
├── templates/                  # Global Django templates (if not using React)
│   └── base.html
│
├── docs/                       # Documentation
│   ├── README.md               # Main project README (the one we designed)
│   ├── documentation.md        # In-depth docs
│   ├── CONTRIBUTING.md
│   └── CODE_OF_CONDUCT.md
│
├── tests/                      # Project-wide tests
│   ├── test_scraper.py
│   ├── test_tech_detection.py
│   └── conftest.py
│
├── .dockerignore
├── .gitignore
├── .env                        # Local environment variables (not committed)
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt            # Python dependencies
├── package.json                # Only if using React in /frontend
├── pyproject.toml              # Optional: for black, isort, etc.
├── LICENSE                     # MIT License
└── README.md                   # Link or symlink to docs/README.md
