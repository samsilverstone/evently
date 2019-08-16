from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    
    message="You are not the user for this view."

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user