from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


CustomUser.groups.field.remote_field.related_name = 'custom_user_groups'
CustomUser.user_permissions.field.remote_field.related_name = 'custom_user_permissions'
