import json
import uuid
from django.test import TransactionTestCase
from api.models import Client


# Create Clients
class ClientTestCase(TransactionTestCase):
    def setUp(self):
        pass

    # Clients can register
    # Registration happens by localhost/api/version/register/ with
    # POST {"first_name": "string", "last_name": "string","email": "email_adress", "passport_number": "string"}
    def register_client(self, email="", passport=""):
        email = email if email else "email " + str(uuid.uuid1())
        passport = passport if passport else "AA012345" + str(uuid.uuid1())
        data = {
                "first_name": "Name",
                "last_name": "Surname",
                "email": email,
                "passport_number": passport
                }
        url = '/api/1/register/'
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        print(response)
        return response

    # newly registered account is inactive until manager approves it
    def test_client_register(self):
        email = "email " + str(uuid.uuid1())
        passport = "AA012345" + str(uuid.uuid1())
        response = self.register_client(email, passport)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(type(response.data["client_id"]) == int)
        self.assertTrue(Client.objects.get(email=email))
        client = Client.objects.get(email=email)
        self.assertTrue(client.status == Client.INACTIVE_OPEN)
        self.assertTrue(client.passport_number == passport)

    def test_client_register_existing(self):
        email = "email " + str(uuid.uuid1())
        passport = "AA012345" + str(uuid.uuid1())
        response = self.register_client(email, passport)
        response = self.register_client(email, passport)
        self.assertTrue(response.status_code == 409)

    def log_in(self, status=""):
        response = self.register_client()
        client_id = response.data["client_id"]
        client = Client.objects.get(id=client_id)
        if not status:
            client.status = Client.ACTIVE
        else:
            client.status = status
        client.save()
        client.refresh_from_db()
        pin_code = client.pin_code
        data = {
                "pin_code": pin_code,
                }
        url = '/api/1/log_in/'
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        return response, client

    # client cannot log in inactive account (mb should get a message)
    def test_client_cannot_log_in_to_inactive_account(self):
        response, _ = self.log_in(Client.INACTIVE_OPEN)
        self.assertTrue(response.status_code == 401)

    # client can log in to an active account by /api/version/login_by_pin_code POST{"pin_code": int_code}
    def test_client_cannot_log_in_to_active_account(self):
        response, _ = self.log_in()
        self.assertTrue(response.status_code == 200)

    def close_client(self):
        response = self.client.put('/api/1/close_account/', json.dumps({}))
        return response

    # Clients can close their account, then account becomes inactive and waits for manager to delete it
    def test_client_close_active_account(self):
        response, client = self.log_in()
        self.assertTrue(response.status_code == 200)
        response = self.close_client()
        self.assertTrue(response.status_code == 200)
        client.refresh_from_db()
        self.assertTrue(client.status == Client.INACTIVE_CLOSED)

    def test_client_get_profile(self):
        response, client = self.log_in()
        self.assertTrue(response.status_code == 200)
        response = self.client.get('/api/1/profile/')
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.data['balance'] == client.balance)
