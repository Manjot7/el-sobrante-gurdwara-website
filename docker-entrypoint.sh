#!/usr/bin/env bash
# Runs on every container start, before gunicorn.
#
# Migrations and seeding happen here rather than in a Fly `release_command`,
# because a release-command machine does not mount the volume — it would
# migrate a throwaway database and leave the real one untouched.
set -o errexit

echo "==> Preparing data directory at ${DJANGO_DATA_DIR:-/app}"
mkdir -p "${DJANGO_DATA_DIR:-/app}/media"

echo "==> Applying database migrations"
python manage.py migrate --noinput

# Both are safe to re-run: they fill in what is missing and never overwrite an
# edit the committee has made.
echo "==> Seeding content"
python manage.py seed_content
python manage.py setup_editors

# Creates the admin login only when the credentials are present as Fly secrets.
# A failure must not stop the site from starting, but it must be loud — a
# silent failure here leaves a working site nobody can log in to.
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]; then
  if SU_OUT=$(python manage.py createsuperuser --noinput 2>&1); then
    echo "==> Admin login created: $DJANGO_SUPERUSER_USERNAME"
  elif echo "$SU_OUT" | grep -qi "already taken\|already exists"; then
    echo "==> Admin login '$DJANGO_SUPERUSER_USERNAME' already exists — left as is."
  else
    echo "########################################################"
    echo "# COULD NOT CREATE THE ADMIN LOGIN"
    echo "# $SU_OUT"
    echo "# The site will still start, but /admin has no account."
    echo "# Most often DJANGO_SUPERUSER_EMAIL is not a valid address."
    echo "# Fix with: fly secrets set DJANGO_SUPERUSER_EMAIL=..."
    echo "########################################################"
  fi
else
  echo "==> DJANGO_SUPERUSER_* not set — skipping admin login creation."
fi

echo "==> Starting web server"
exec "$@"
