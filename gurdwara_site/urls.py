from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
]

# Committee-uploaded photos.
#
# django.conf.urls.static.static() silently returns [] when DEBUG is False, so
# it cannot be used to serve media in production — every uploaded photo would
# 404. WhiteNoise doesn't cover this either: it only serves STATIC_ROOT.
#
# Serving media through Django is not the fastest option, but at this site's
# traffic (a few hundred visits a week, images already resized on upload) it is
# perfectly adequate and keeps the deployment to a single service. Put the
# media directory behind a CDN or nginx if that ever stops being true.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        )
    ]
