from django.urls import path
from . import views

urlpatterns = [
    path("encrypt/", views.getEncryption),
    path("decrypt/", views.getDecryption),
    path("sign/", views.getSignature),
    path("verify/", views.getVerification),
]
