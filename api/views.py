# -*- coding: utf-8 -*-
import api.client as client
import api.manager as manager
import json
# from __future__ import unicode_literals

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Client


@api_view(['GET'])
def index(request):
    return Response({"message": "Hello world!"})


@api_view(['POST'])
def register_client(request, version):
    body = json.loads(request.body.decode("utf-8"))
    client_id, pin_code, message = client.register(body)
    content = {"client_id": client_id, "message": message, "pin_code": pin_code}
    print(message)
    response_status = status.HTTP_200_OK if client_id else status.HTTP_409_CONFLICT
    return Response(content, status=response_status)


@api_view(['POST'])
def log_in_client(request, version):
    body = json.loads(request.body.decode("utf-8"))
    pin_code = body['pin_code']
    user = client.get_user_to_log_in(pin_code)
    if user:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@login_required
def close_account(request, version):
    client.close_account(request.user)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@login_required
def client_profile(request, version):
    return Response({"balance": client.get_balance(request.user)}, status=status.HTTP_200_OK)


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


@api_view(['GET'])
@login_required
def manager_pending_accounts(request, version):
    if is_manager(request.user):
        client_list = manager.get_pending_list()
        return Response({'client_list': client_list}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@login_required
def manager_approve_active(request, version, client_id):
    if is_manager(request.user):
        manager.approve(client_id, Client.ACTIVE)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@login_required
def manager_approve_delete(request, version, client_id):
    if is_manager(request.user):
        manager.approve(client_id, Client.DELETED)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

