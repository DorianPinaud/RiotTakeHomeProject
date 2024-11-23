from .test_setup import TestSetup
import time


class TestViews(TestSetup):

    def test_basic_encoding(self):
        time.sleep(1)
        response = self.client.post(
            self.encrypt_url, data=self.basic_data_to_encode, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.basic_data_to_decode)

    def test_basic_decoding(self):
        time.sleep(1)
        response = self.client.post(
            self.decrypt_url, data=self.basic_data_to_decode, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.basic_data_to_encode)

    def test_rate_limit_exceeded_for_encoding(self):
        time.sleep(1)
        response = None
        for i in range(61):
            response = self.client.post(
                self.encrypt_url, data=self.basic_data_to_encode, format="json"
            )
        self.assertEqual(response.status_code, 401)

    def test_exact_rate_limit_for_decoding(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(
                self.decrypt_url, data=self.basic_data_to_decode, format="json"
            )
        self.assertEqual(response.status_code, 200)

    def test_exact_rate_limit_for_encoding(self):
        time.sleep(1)
        response = None
        for i in range(60):
            response = self.client.post(
                self.encrypt_url, data=self.basic_data_to_encode, format="json"
            )
        self.assertEqual(response.status_code, 200)
