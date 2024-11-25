from rest_framework.test import APITestCase
from django.urls import reverse
import time


class RateLimitTesting(APITestCase):
    def setUp(self):
        self.encrypt_url = reverse("encrypt")
        self.decrypt_url = reverse("decrypt")
        self.sign_url = reverse("sign")
        self.verify_url = reverse("verify")
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_rate_limit_exceeded_for_encoding(self):
        time.sleep(1)
        response = None
        for i in range(61):
            response = self.client.post(self.encrypt_url, data={}, format="json")
        self.assertEqual(response.status_code, 429)

    def test_rate_limit_exceeded_for_decoding(self):
        time.sleep(1)
        response = None
        for i in range(61):
            response = self.client.post(self.decrypt_url, data={}, format="json")
        self.assertEqual(response.status_code, 429)

    def test_exact_rate_limit_for_decoding(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(self.decrypt_url, data={}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_exact_rate_limit_for_encoding(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(self.encrypt_url, data={}, format="json")
        self.assertEqual(response.status_code, 200)
