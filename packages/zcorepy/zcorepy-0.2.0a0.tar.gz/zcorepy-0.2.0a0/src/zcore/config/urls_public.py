from django.urls import path, include
from django.urls import re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from zcore.apps.shared.platformauth.views import (
    PlatformUserLoginView,
)

urlpatterns = [
    re_path(
        r"^admin/login/$",
        PlatformUserLoginView.as_view(),
        name="login",
    ),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^api/", include("zcore.api.platform.urls")),
    re_path(r"api/auth/", include("knox.urls")),
    re_path(r"session_security/", include("session_security.urls")),
    re_path(r"^", include("zcore.apps.shared.tenancy.urls")),
]
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
