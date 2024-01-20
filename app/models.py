from django.db import models
from django.utils.translation import gettext as _

from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    # class RoleType(models.TextChoices):
    #     ADMIN = "Admin", _("admin")
        
    
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    # role = models.CharField(max_length=100, null=True, blank=True, choice=)