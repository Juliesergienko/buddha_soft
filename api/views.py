# -*- coding: utf-8 -*-
import api.client as client
import api.manager as manager
import json
# from __future__ import unicode_literals

from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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
def close_account(request, version):
    if request.user.is_authenticated():
        client.close_account(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
