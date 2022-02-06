from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allows user to only view their own information
    """

    def has_object_permission(self, request, view, obj):
        return request.method == "GET" and obj.email == request.user.email

    def has_permission(self, request, view):
        return view.action != "list" and request.method == "GET"
