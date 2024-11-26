from django.urls import path
from . import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path("encrypt/", views.encryption_endpoint, name="encrypt"),
    path("decrypt/", views.decryption_endpoint, name="decrypt"),
    path("sign/", views.signing_endpoint, name="sign"),
    path("verify/", views.verification_endpoint, name="verify"),
    # Documentation path
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
