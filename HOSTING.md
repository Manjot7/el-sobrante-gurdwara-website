# Hosting options

The site is now a real Django app with a database and photo uploads, so it
needs somewhere that runs Python and keeps files between deploys.

## Why the free tiers don't work here

Free tiers give you an **ephemeral filesystem**. Every redeploy — and on some
hosts every daily restart — wipes it back to what's in Git. The database and
every photo the committee uploaded go with it. That defeats the entire point
of putting photos in the admin.

Free tiers also sleep after ~15 minutes idle, so the first visitor of the
morning waits up to a minute for the page. For a gurdwara website that's the
sangat checking the livestream time.

Anything chosen must therefore have a **persistent disk** (or external file
storage).

## Options

| Host | ~Cost/mo | Setup | Maintenance | Notes |
|---|---|---|---|---|
| **Render Starter** ⭐ | **$7** | Easy | Low | Persistent disk add-on holds SQLite + photos. Deploys from GitHub on push. What the project is currently configured for. |
| Railway | $5–10 | Easy | Low | Volumes work the same way. Usage-based billing, so cost drifts with traffic. |
| PythonAnywhere | $5 | Moderate | Low | Real persistent disk, no cold starts, very stable. Deploys are manual (pull + reload) rather than automatic. |
| DigitalOcean App Platform | $5–12 | Moderate | Medium | Needs a separate managed database or volume; more moving parts than this site warrants. |
| DigitalOcean Droplet / VPS | $6 | Hard | **High** | You own OS updates, nginx, certificates, backups. Only worth it if a volunteer genuinely enjoys sysadmin work. |
| Free tiers (Render/Fly free) | $0 | Easy | — | **Not viable.** Uploaded photos are deleted on redeploy. |

⭐ **Recommendation: Render Starter, ~$7/month.**

It's the least to think about: push to GitHub and it deploys, the disk keeps
the photos, and there's no separate database service to pay for or patch.

## Why SQLite and not Postgres

Four small tables and one or two editors. A managed Postgres instance would
roughly double the monthly cost and add another service to keep alive, for a
database that will hold a few hundred rows. SQLite on the persistent disk is
the simpler and cheaper fit, and it can be moved to Postgres later without
touching the models if the site ever outgrows it.

## Render setup, in short

1. New → Web Service, connect the GitHub repo
2. Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start: `gunicorn gurdwara_site.wsgi`
4. Add a **Disk**, mount path `/data`, 1 GB is plenty
5. Environment variables:
   - `DJANGO_DATA_DIR=/data` — puts the database and photos on the disk
   - `DJANGO_SECRET_KEY` — generate a long random string
   - `DJANGO_DEBUG=false`
   - `DJANGO_ALLOWED_HOSTS=thesikhcenter.com,www.thesikhcenter.com`
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://thesikhcenter.com,https://www.thesikhcenter.com`
6. Create the first login: `python manage.py createsuperuser`
7. Create the editor group: `python manage.py setup_editors`
8. Point the domain at Render and let it issue the certificate

## Backups

The whole site is one file: `/data/db.sqlite3`, plus the `/data/media` folder.
Download both periodically — that is a complete backup. Worth doing monthly,
and definitely before any handover.
