#!/usr/bin/env bash
# Render build step. Runs on every deploy.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Both are safe to re-run: they fill in what is missing and never overwrite an
# edit. On the free tier the disk is wiped on every deploy, so this is what
# brings the history photos and daily programme back each time.
python manage.py seed_content
python manage.py setup_editors

# Creates the admin login only if DJANGO_SUPERUSER_USERNAME / _EMAIL /
# _PASSWORD are set in the host's environment. Set them in the Render
# dashboard — the password never goes near this repo.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --noinput || echo "superuser already exists"
fi
