from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomAdmin(UserAdmin):
    list_display=['id','full_name','username','is_staff']