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
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_only_dictionary_should_be_encodable__test_on_list(self):
        response = self.client.post(self.encrypt_url, data=[1, 2, 3], format="json")
        self.assertEqual(response.status_code, 400)

    def test_only_dictionary_should_be_encodable__test_on_number(self):
        response = self.client.post(self.encrypt_url, data=10, format="json")
        self.assertEqual(response.status_code, 400)

    def test_only_dictionary_should_be_encodable__test_on_str(self):
        response = self.client.post(self.encrypt_url, data="10", format="json")
        self.assertEqual(response.status_code, 400)

    def test_decrypt_corrupted_data__none_string_data(self):
        response = self.client.post(
            self.decrypt_url,
            data={
                "bar": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_decrypt_corrupted_data__none_special_character(self):
        response = self.client.post(
            self.decrypt_url,
            data={
                "bar": "@@@@",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_algorithm__not_the_good_encoding(self):
        response = self.client.post(
            f"{self.decrypt_url}?algo=base64",
            data={
                "foo": "22666f6f62617222",
                "bar": "7b226973426172223a20747275657d",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_algorithm__not_exiting_algo(self):
        response = self.client.post(
            f"{self.decrypt_url}?algo=toto",
            data={
                "foo": "ImZvb2JhciI=",
                "bar": "eyJpc0JhciI6IHRydWV9",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_verify_form(self):
        response = self.client.post(
            f"{self.verify_url}",
            data={
                "sign": "11b1a6f65d485323498c0daf5c8c3b82b4a3eeed45992c2d8aaf52069a3837f2",
                "d": {"foo": "foobar", "bar": {"isBar": True}},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
