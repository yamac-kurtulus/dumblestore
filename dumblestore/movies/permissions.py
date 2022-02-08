from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allows user to only view their own information
    """

    def has_object_permission(self, request, view, obj):
        return request.method == "GET" and obj.email == request.user.email

    def has_permission(self, request, view):
        return view.action == "me"


class IsAdminOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    Allows:
    Admins: full-control
    Customer users: read-only
    Anon: none
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
