# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from strawberry.django.views import GraphQLView

from config.schema import schema

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/", include("allauth.urls")),
    # GraphQL endpoint.
    # CSRF-exempted for now since the Next.js frontend doesn't yet send the
    # CSRF header on mutations. Session cookies still protect authentication
    # itself (you can't forge someone else's session), but CSRF exemption
    # means a malicious site could trigger state-changing mutations on behalf
    # of a logged-in user if they visit it while authenticated. Revisit this
    # before anything beyond local development — the fix is either (a) have
    # the Next.js client read the csrftoken cookie and send it back as
    # X-CSRFToken on every request, or (b) move to a non-cookie auth scheme.
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                schema=schema,
                multipart_uploads_enabled=True,  # required for Upload scalar / file uploads
            )
        ),
    ),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            *urlpatterns,
        ]