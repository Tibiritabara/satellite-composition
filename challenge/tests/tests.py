import os
import json
from rest_framework.test import APITransactionTestCase


class POSTRequest(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        if os.path.exists("challenge/tests/resources/generated/T33UUP_20180804Tvisible.jpg"):
            os.remove("challenge/tests/resources/generated/T33UUP_20180804Tvisible.jpg")

    def test_without_body(self):
        response = self.client.post('/generate-image')
        assert (response.status_code == 400)

    def test_with_invalid_json(self):
        json_file = open('challenge/tests/resources/invalid_json.json')
        body_dict = json.load(json_file)
        response = self.client.post('/generate-image', body_dict, format='json')
        assert (response.status_code == 400)

    def test_with_unavailable_data(self):
        json_file = open('challenge/tests/resources/unavailable_data.json')
        body_dict = json.load(json_file)
        response = self.client.post('/generate-image', body_dict, format='json')
        assert (response.status_code == 412)

    def test_success(self):
        json_file = open('challenge/tests/resources/successful_json.json')
        body_dict = json.load(json_file)
        response = self.client.post('/generate-image', body_dict, format='json')
        print(response.status_code)
        assert (response.status_code == 200)
