# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    INACTIVE_OPEN = "IO"
    INACTIVE_CLOSED = "IC"
    ACTIVE = "A"
    DELETED = "D"
    ACCOUNT_CHOICES = (
            (INACTIVE_OPEN, "inactive_open"),
            (INACTIVE_CLOSED, "inactive_closed"),
            (ACTIVE, "active"),
            (DELETED, "deleted")
            )
    user = models.OneToOneField(User)
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    passport_number = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=2, choices=ACCOUNT_CHOICES)
    pin_code = models.CharField(unique=True, max_length=255)
    balance = models.DecimalField(decimal_places=2, max_digits=10)
