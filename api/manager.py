from api.models import Client
from django.db.models import Q
from django.shortcuts import get_object_or_404


def get_pending_list():
    result = [{
        'id': client.id,
        'status': client.status
        } for client in Client.objects.filter(Q(status=Client.INACTIVE_OPEN) | Q(status=Client.INACTIVE_CLOSED))]
    return result


def approve(client_id, status):
    client = get_object_or_404(Client, id=client_id)
    client.status = status
    client.save()
