import json
from django.test import TransactionTestCase
from api.tests.clients import ClientTestCase
from api.models import Client
from django.contrib.auth.models import User, Group


class ManagerTestCase(TransactionTestCase):
    def setUp(self):
        self.manager_user = User.objects.create(username='manager', password='manager')
        group = Group(name='Manager')
        group.save()
        self.manager_user.groups.add(group)
        self.manager_user.save()

    # Managers can get a list of pending accounts for approve
    def test_manager_get_pending_accounts(self):
        client_ids = [ClientTestCase.register_client(self).data['client_id'] for i in range(5)]
        clients = [Client.objects.get(id=client_id) for client_id in client_ids]
        for i in range(3):
            clients[i].status = Client.INACTIVE_CLOSED
            clients[i].save()
        self.client.force_login(self.manager_user)
        response = self.client.get('/api/1/pending_accounts/')
        self.assertTrue(response.status_code == 200)
        clients = response.data['client_list']
        self.assertTrue(len(clients) == 5)
        self.assertTrue(len([client for client in clients if client['status'] == Client.INACTIVE_CLOSED]) == 3)
        self.assertTrue(len([client for client in clients if client['status'] == Client.INACTIVE_OPEN]) == 2)

    # Managers can approve accouts one by one
    def test_manager_approves_account(self):
        self.client.force_login(self.manager_user)
        client_id = ClientTestCase.register_client(self).data['client_id']
        response = self.client.put('/api/1/approve/' + str(client_id) + '/active/', json.dumps({}))
        self.assertTrue(response.status_code == 200)
        client = Client.objects.get(id=client_id)
        self.assertTrue(client.status == Client.ACTIVE)
        client.status = Client.INACTIVE_CLOSED
        client.save()
        response = self.client.put('/api/1/approve/' + str(client_id) + '/delete/', json.dumps({}))
        self.assertTrue(response.status_code == 200)
        client.refresh_from_db()
        self.assertTrue(client.status == Client.DELETED)
