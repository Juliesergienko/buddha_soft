import uuid
from api.models import User, Client


def register(body):
    try:
        pin_code = uuid.uuid1()
        user = User.objects.create(
                username=body['first_name'] + body['last_name'],
                password=pin_code
                )
        client = Client.objects.create(
                user=user,
                first_name=body['first_name'],
                last_name=body['last_name'],
                email=body['email'],
                passport_number=body['passport_number'],
                status=Client.INACTIVE_OPEN,
                pin_code=pin_code,
                balance=10.99
                )
        message = "New client created"
        return client.id, pin_code, message
    except Exception as e:
        return None, None, str(e)


def get_user_to_log_in(pin_code):
    try:
        client = Client.objects.get(pin_code=pin_code)
        if client.status == Client.ACTIVE:
            return client.user
        else:
            return None
    except Exception as e:
        return None

def close_account(user):
    client = Client.objects.get(user=user)
    client.status = Client.INACTIVE_CLOSED
    client.save()
    
