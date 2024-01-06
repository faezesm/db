from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from . models import Cryptocurrency

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self , request , view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user