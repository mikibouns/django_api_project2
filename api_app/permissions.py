from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be owner of this object'
    my_safe_method = ['GET', 'PATCH', 'POST', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.addedBy == request.user or obj == request.user or request.user.is_superuser


class IsOwnerOrReadOnlyKeyWords(IsOwnerOrReadOnly):
    my_safe_method = ['GET', 'PATCH', 'POST', 'DELETE']

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.personID.addedBy == request.user or request.user.is_superuser


class IsOwnerOrReadOnlyPages(IsOwnerOrReadOnly):
    my_safe_method = ['GET', 'PATCH', 'POST', 'DELETE']

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.siteID.addedBy == request.user or request.user.is_superuser