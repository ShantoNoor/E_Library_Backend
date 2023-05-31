from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  
        return obj.user_id == request.user.id or request.user.is_staff
    

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  
        return obj.user_id == request.user.id

class BookIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  
        return obj.added_by.id == request.user.id