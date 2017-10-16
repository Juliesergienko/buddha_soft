import json
import uuid
from django.test import TestCase
from api.models import Client
from rest_framework.test import APIRequestFactory


# Create Clients
class ClientTestCase(TestCase):
    def setUp(self):
        self.request = APIRequestFactory()

    # Clients can register
    # Registration happens by localhost/api/version/register/ with
    # POST {"first_name": "string", "last_name": "string","email": "email_adress", "passport_number": "string"}
    def test_client_register(self):
        email = "email " + str(uuid.uuid1())
        passport = "AA012345" + str(uuid.uuid1())
        data = {
                "first_name": "Name",
                "last_name": "Surname",
                "email": email,
                "passport_number": passport
                }
        url = '/api/1/register/'
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertTrue(response.status_code == 200)
        print(response.data['message'])
        self.assertTrue(type(response.data["client_id"]) == int)
        self.assertTrue(Client.objects.get(email=email))

    # newly registered account is inactive until manager approves it
    # client can log in to an active account by /api/login_by_pin_code POST{"pin_code": int_code}
    # client cannot log in inactive account (mb should get a message)
    # Clients can close their account, then account becomes inactive and waits for manager to delete it

