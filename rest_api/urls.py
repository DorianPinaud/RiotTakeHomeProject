from django.urls import path
from . import views

urlpatterns = [
    path("encrypt/", views.encryption_endpoint, name="encrypt"),
    path("decrypt/", views.decryption_endpoint, name="decrypt"),
    path("sign/", views.signing_endpoint, name="sign"),
    path("verify/", views.verification_endpoint, name="verify"),
]
