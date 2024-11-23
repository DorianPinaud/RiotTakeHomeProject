from django.urls import path
from . import views

urlpatterns = [
    path("encrypt/", views.encryption_endpoint, name="encrypt"),
    path("decrypt/", views.decryption_endpoint, name="decrypt"),
    path("sign/", views.getSignature, name="sign"),
    path("verify/", views.getVerification, name="verify"),
]
