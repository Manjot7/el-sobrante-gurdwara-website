"""
Render all 5 pages to static HTML in docs/ for GitHub Pages.
Run with: python build_static.py
"""
import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gurdwara_site.settings")

import django
django.setup()

from django.test import Client

BASE_URL = "https://manjot7.github.io/el-sobrante-gurdwara-website"

PAGES = {
    "/":             "index.html",
    "/schedule/":    "schedule/index.html",
    "/school/":      "school/index.html",
    "/livestream/":  "livestream/index.html",
    "/contact/":     "contact/index.html",
}

# Root-relative nav links → base-relative so <base href> resolves them correctly
# from any subdirectory page.
LINK_FIXES = [
    ('href="/"',             'href="./"'),
    ('href="/schedule/"',    'href="schedule/"'),
    ('href="/school/"',      'href="school/"'),
    ('href="/livestream/"',  'href="livestream/"'),
    ('href="/contact/"',     'href="contact/"'),
    ("href='/'",             "href='./'"),
    ("href='/schedule/'",    "href='schedule/'"),
    ("href='/school/'",      "href='school/'"),
    ("href='/livestream/'",  "href='livestream/'"),
    ("href='/contact/'",     "href='contact/'"),
]


def fix_html(html: str) -> str:
    for old, new in LINK_FIXES:
        html = html.replace(old, new)
    # Inject <base> so relative links resolve from the repo root regardless
    # of which subdirectory the page lives in.
    html = html.replace(
        "<head>",
        f'<head>\n  <base href="{BASE_URL}/">',
        1,
    )
    return html


client = Client()
docs = Path("docs")
docs.mkdir(exist_ok=True)

# Prevent Jekyll from mangling the output on GitHub Pages
(docs / ".nojekyll").touch()

for url, filename in PAGES.items():
    response = client.get(url)
    html = fix_html(response.content.decode("utf-8"))
    out = docs / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  {url:20s} -> docs/{filename}")

print("Static build complete."  )
