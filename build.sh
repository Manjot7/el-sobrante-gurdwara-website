#!/usr/bin/env bash
# Render build step. Runs on every deploy.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Both are safe to re-run: they fill in what is missing and never overwrite an
# edit. On the free plan the disk is wiped on every deploy, so this is what
# brings the history photos and daily programme back each time.
python manage.py seed_content
python manage.py setup_editors

# Creates the admin login from DJANGO_SUPERUSER_USERNAME / _EMAIL / _PASSWORD,
# which are set in the host's dashboard so the password never enters this repo.
#
# A failure here must not kill the deploy — but it must be loud. Getting this
# wrong silently (a mistyped email is enough for Django to reject it) would
# leave a site that looks fine and cannot be logged into.
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]; then
  if SUPERUSER_OUTPUT=$(python manage.py createsuperuser --noinput 2>&1); then
    echo "Admin login created: $DJANGO_SUPERUSER_USERNAME"
  elif echo "$SUPERUSER_OUTPUT" | grep -qi "already taken\|already exists"; then
    echo "Admin login '$DJANGO_SUPERUSER_USERNAME' already exists — left as is."
  else
    echo "########################################################"
    echo "# COULD NOT CREATE THE ADMIN LOGIN"
    echo "#"
    echo "# $SUPERUSER_OUTPUT"
    echo "#"
    echo "# The website will still deploy, but /admin will have no"
    echo "# account to log in with."
    echo "#"
    echo "# Most often this is DJANGO_SUPERUSER_EMAIL not being a"
    echo "# valid address. Fix it in the dashboard and redeploy."
    echo "########################################################"
  fi
else
  echo "DJANGO_SUPERUSER_* not set — skipping admin login creation."
fi
