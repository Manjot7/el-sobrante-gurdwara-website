# Fly.io image for the Sikh Center website.
#
# Python 3.13 because Django 6 needs 3.12 or newer. The slim image is enough:
# Pillow, gunicorn and whitenoise all ship manylinux wheels, so there is no
# compiler needed and nothing to apt-get.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files into the image at build time, so starting a container
# is fast and does not depend on the volume.
#
# DJANGO_DEBUG must be false here. With DEBUG on, settings.py picks the plain
# static files backend, no staticfiles.json manifest is written, and the app
# then crashes at runtime when the manifest backend goes looking for it. The
# key below is a throwaway used only for this build step.
RUN DJANGO_DEBUG=false \
    DJANGO_SECRET_KEY=build-time-only-not-used-at-runtime-0000000000 \
    python manage.py collectstatic --noinput

RUN chmod +x docker-entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "gurdwara_site.wsgi:application", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
