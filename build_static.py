"""
Render the site to static HTML in docs/ for any static host.
Run with: python build_static.py

This is a *snapshot* of whatever is in the database when it runs. It's for
showing people the site without standing up a server — the admin, photo
uploads and the calendar all need the real Django app.

Output uses relative paths only, with no <base> tag, so the docs/ folder can
be dropped on GitHub Pages, Netlify, or opened from disk without changes.
"""
import os
import re
import shutil
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gurdwara_site.settings")

import django
django.setup()

from django.conf import settings
from django.test import Client

# url -> output path. The depth of the output path decides how many "../"
# steps are needed to get back to the root.
PAGES = {
    "/":            "index.html",
    "/schedule/":   "schedule/index.html",
    "/events/":     "events/index.html",
    "/academy/":    "academy/index.html",
    "/livestream/": "livestream/index.html",
    "/contact/":    "contact/index.html",
}

ROUTES = ["schedule", "events", "academy", "livestream", "contact"]


def to_relative(html: str, depth: int) -> str:
    """Rewrite root-relative URLs to paths relative to this page."""
    prefix = "../" * depth

    for route in ROUTES:
        html = html.replace(f'href="/{route}/"', f'href="{prefix}{route}/"')
        html = html.replace(f"href='/{route}/'", f"href='{prefix}{route}/'")

    # Home link: "./" at the root, "../" from a subdirectory.
    html = html.replace('href="/"', f'href="{prefix or "./"}"')
    html = html.replace("href='/'", f"href='{prefix or './'}'")

    # Assets, in any attribute (src=, href=, content=).
    html = re.sub(r'(["\'])/(static|media)/', rf'\1{prefix}\2/', html)

    return html


docs = Path("docs")
docs.mkdir(exist_ok=True)
(docs / ".nojekyll").touch()  # stop Jekyll mangling the output on GitHub Pages

client = Client()
for url, filename in PAGES.items():
    response = client.get(url)
    if response.status_code != 200:
        raise SystemExit(f"  {url} returned {response.status_code} — aborting")
    out = docs / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    depth = len(Path(filename).parts) - 1
    out.write_text(
        to_relative(response.content.decode("utf-8"), depth), encoding="utf-8"
    )
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

print("\nStatic build complete. The docs/ folder works on any static host.")
