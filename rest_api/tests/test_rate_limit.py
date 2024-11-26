from rest_framework.test import APITestCase
from django.urls import reverse
import time


class RateLimitTesting(APITestCase):
    def setUp(self):
        self.encrypt_url = reverse("encrypt")
        self.decrypt_url = reverse("decrypt")
        self.sign_url = reverse("sign")
        self.verify_url = reverse("verify")

        self.basic_verify_form = {
            "signature": "11b1a6f65d485323498c0daf5c8c3b82b4a3eeed45992c2d8aaf52069a3837f2",
            "data": {"foo": "foobar", "bar": {"isBar": True}},
        }
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

    def test_exact_rate_limit_for_signing(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(self.sign_url, data={}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_rate_limit_exceeded_for_signing(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(self.sign_url, data={}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_exact_rate_limit_for_verifying(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(
                self.verify_url, data=self.basic_verify_form, format="json"
            )
        self.assertEqual(response.status_code, 200)

    def test_rate_limit_exceeded_for_verifying(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(
                self.verify_url, data=self.basic_verify_form, format="json"
            )
        self.assertEqual(response.status_code, 200)
