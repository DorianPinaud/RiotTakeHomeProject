from rest_framework.test import APITestCase
from django.urls import reverse
import time
import os


class BasicFeatureTesting(APITestCase):
    def setUp(self):
        self.encrypt_url = reverse("encrypt")
        self.decrypt_url = reverse("decrypt")
        self.sign_url = reverse("sign")
        self.verify_url = reverse("verify")

        os.environ["SECRET_KEY"] = "test_secret_key"
        self.basic_data_to_encode = {"foo": "foobar", "bar": {"isBar": True}}
        self.basic_data_to_decode = {
            "foo": "ImZvb2JhciI=",
            "bar": "eyJpc0JhciI6IHRydWV9",
        }
        self.basic_data_to_decode_with_hex_algo = {
            "foo": "22666f6f62617222",
            "bar": "7b226973426172223a20747275657d",
        }
        self.signature = (
            "11b1a6f65d485323498c0daf5c8c3b82b4a3eeed45992c2d8aaf52069a3837f2"
        )
        self.basic_verify_form = {
            "signature": "11b1a6f65d485323498c0daf5c8c3b82b4a3eeed45992c2d8aaf52069a3837f2",
            "data": {"foo": "foobar", "bar": {"isBar": True}},
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_basic_encoding(self):
        response = self.client.post(
            self.encrypt_url, data=self.basic_data_to_encode, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.basic_data_to_decode)

    def test_basic_decoding(self):
        response = self.client.post(
            self.decrypt_url, data=self.basic_data_to_decode, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.basic_data_to_encode)

    def test_hex_encoding(self):
        response = self.client.post(
            self.encrypt_url + "?algo=hex",
            data=self.basic_data_to_encode,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.basic_data_to_decode_with_hex_algo)

    def test_hex_decoding(self):
        response = self.client.post(
            self.decrypt_url + "?algo=hex",
            data=self.basic_data_to_decode_with_hex_algo,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.basic_data_to_encode)

    def test_signature(self):
        response = self.client.post(
            self.sign_url, data=self.basic_data_to_encode, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.signature)
