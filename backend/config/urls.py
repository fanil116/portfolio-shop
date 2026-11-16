from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from common.healthcheck_view import healthcheck_view

from .routers import router

# Заголовки админки задаются в settings.UNFOLD
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("healthcheck/", healthcheck_view, name="healthcheck"),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [path("api/__debug__/", include(debug_toolbar.urls))]
    # В production медиа отдаёт nginx
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.API_DOCS_ENABLE:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    ]
