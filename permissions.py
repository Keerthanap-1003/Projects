from rest_framework import permissions

class ManagerStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userType in ['staff', 'manager']

class ManagerAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userType in ['manager','admin'] 
    
#Permission class to list managers.admin can list mangers
class Admin(permissions.BasePermission):
    
    def has_permission(self, request, view):
         if not request.user.is_authenticated:
             return False 
         return request.user.userType == 'admin'

class Staff(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userType in ['staff']

class Customer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userType == 'customer'
