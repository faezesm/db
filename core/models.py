from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    full_name = models.CharField(_("full_name"), max_length=255,help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),)

