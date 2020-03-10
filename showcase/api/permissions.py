from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
        return obj.user == request.user


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
        return obj.administrator.filter(pk=request.user.pk).exists()


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.administrator.filter(pk=request.user.pk).exists()


class IsAdminOrOwner(permissions.BasePermission):
    '''
    permission for collaborators to delete collaborations
    - check done on collaborator level
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
        return obj.user == request.user or obj.post.administrator.filter(pk=request.user.pk).exists()