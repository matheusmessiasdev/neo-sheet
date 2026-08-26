from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(request.user)
        print('OBJETO ABAIXO')
        print('OBJETO ABAIXO')
        print('OBJETO ABAIXO')
        print('OBJETO ABAIXO')
        print(obj)
        print(obj.user)
        return request.user == obj.user
    ...
