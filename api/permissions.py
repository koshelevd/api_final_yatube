"""DRF API permission classes of the 'posts' app."""
from rest_framework.permissions import (BasePermission, IsAuthenticated,
                                        SAFE_METHODS)


class ResourcePermission(BasePermission):
    """
    Permission class.

    Check resource's ownership and method's safety.
    """

    def has_object_permission(self, request, view, obj):
        """
        Override has_object_permission method.

        Return True if authorized user is owner of the resource or if method
        is safe.
        """
        return request.user == obj.author or request.method in SAFE_METHODS
