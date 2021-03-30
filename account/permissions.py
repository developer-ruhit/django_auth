from rest_framework.permissions import BasePermission
class IsAccountOwner(BasePermission):
    def has_object_permission(self,request,obj,view):
        return request.user.id==obj.id