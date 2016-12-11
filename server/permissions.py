import json

from rest_framework import permissions

__author__ = 'Nem'

from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        user = request.user
        return user.is_staff


class IsAuthenticatedOrCreate(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)

class SaveFirstShowThenRequireAuthentication(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if not request.user.is_authenticated():
                if len(request.data['data']['content']) < 2:
                    return True
            else:
                return request.user and request.user.is_authenticated()
