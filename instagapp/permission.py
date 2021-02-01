from rest_framework.permissions import BasePermission


class CustomUserPermission(BasePermission):

    def has_permission(self,request,view):
        if request.method=='POST':
            return True
        if request.user.is_authenticated:
            return True
    
    def has_object_permission(self,request,view,obj):
        if obj.id==request.user.id:
            return True
    