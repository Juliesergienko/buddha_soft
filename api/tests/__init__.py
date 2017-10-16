# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from api.tests.urls import *
from api.tests.clients import *
from api.tests.managers import *

# Create your tests here.

# Create Clients
# Clients can register
# Registration happens by localhost/api/register with
# POST {"first_name": "string", "last_name": "string","email": "email_adress", "passport_number": "string"}
# newly registered account is inactive until manager approves it
# Clients can get pin code
# Clients can log in by pin code
# client can log in to an active account by /api/login_by_pin_code POST{"pin_code": int_code}
# client cannot log in inactive account (mb should get a message)

# Clients can close their account, then account becomes inactive and waits for manager to delete it
# Create Managers
# Managers are added by SuperAdmin
# Managers can get a list of pending accounts for approve
# Managers can approve accouts one by one
# Managers can get a list of accounts to close
# Managers can close an account
# Email Notifications to Managers
# Email Notifications to Clients
