# -*- coding: utf-8 -*-
import api.client as client
import api.manager as manager
import json
# from __future__ import unicode_literals

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def index(request):
    return Response({"message": "Hello world!"})


@api_view(['POST'])
def register_client(request, version):
    print(request.body)
    body = json.loads(request.body.decode("utf-8"))
    print(body)
    client_id, pin_code, message = client.register(body)
    content = {"client_id": client_id, "message": message, "pin_code": pin_code}
    return Response(content, status=status.HTTP_200_OK)
