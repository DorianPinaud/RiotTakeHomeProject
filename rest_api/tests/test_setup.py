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

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
