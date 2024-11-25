from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetup(APITestCase):

    def setUp(self):
        self.encrypt_url = reverse("encrypt")
        self.decrypt_url = reverse("decrypt")

        self.basic_data_to_encode = {"foo": "foobar", "bar": {"isBar": True}}
        self.basic_data_to_decode = {
            "foo": "ImZvb2JhciI=",
            "bar": "eyJpc0JhciI6IHRydWV9",
        }
        self.basic_data_to_decode_with_hex_algo = {
            "foo": "22666f6f62617222",
            "bar": "7b226973426172223a20747275657d",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
