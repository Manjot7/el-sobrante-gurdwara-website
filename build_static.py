"""
Render the site to static HTML in docs/ for GitHub Pages.
Run with: python build_static.py

This exists to give the committee a clickable link during review without
standing up a server. It is a *snapshot* of whatever is in the database at the
time it runs — the admin, the calendar sync and photo uploads all need the real
Django app. Retire this once the site is live on a proper host.
"""
import os
import shutil
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gurdwara_site.settings")

import django
django.setup()

from django.conf import settings
from django.test import Client

BASE_URL = "https://manjot7.github.io/el-sobrante-gurdwara-website"

PAGES = {
    "/":             "index.html",
    "/schedule/":    "schedule/index.html",
    "/events/":      "events/index.html",
    "/academy/":     "academy/index.html",
    "/livestream/":  "livestream/index.html",
    "/contact/":     "contact/index.html",
}

# Root-relative URLs → base-relative, so <base href> resolves them correctly
# from any subdirectory page.
LINK_FIXES = [
    ('href="/"',             'href="./"'),
    ("href='/'",             "href='./'"),
]
for route in ("schedule", "events", "academy", "livestream", "contact"):
    LINK_FIXES.append((f'href="/{route}/"', f'href="{route}/"'))
    LINK_FIXES.append((f"href='/{route}/'", f"href='{route}/'"))
# Uploaded photos and icons live alongside the pages in docs/.
LINK_FIXES += [
    ('="/static/', '="static/'),
    ('="/media/',  '="media/'),
]


def fix_html(html: str) -> str:
    for old, new in LINK_FIXES:
        html = html.replace(old, new)
    return html.replace("<head>", f'<head>\n  <base href="{BASE_URL}/">', 1)


docs = Path("docs")
docs.mkdir(exist_ok=True)
(docs / ".nojekyll").touch()  # stop Jekyll mangling the output

client = Client()
for url, filename in PAGES.items():
    response = client.get(url)
    if response.status_code != 200:
        raise SystemExit(f"  {url} returned {response.status_code} — aborting")
    out = docs / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(fix_html(response.content.decode("utf-8")), encoding="utf-8")
    print(f"  {url:14s} -> docs/{filename}")

# Without these the snapshot has no favicon and no photos.
for label, source, dest in [
    ("static", Path(settings.STATICFILES_DIRS[0]), docs / "static"),
    ("media", Path(settings.MEDIA_ROOT), docs / "media"),
]:
    if not source.exists():
        print(f"  {label}: nothing at {source}, skipped")
        continue
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(source, dest)
    count = sum(1 for _ in dest.rglob("*") if _.is_file())
    print(f"  {label:14s} -> docs/{dest.name}/ ({count} files)")

print("Static build complete.")
