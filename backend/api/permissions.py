from rest_framework import permissions

class IsOwner (permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST':
            return True
        
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        print("OBJ USER:", obj.user)
        print("REQUEST USER:", request.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.role == 'elder':
            return obj.user == request.user
        
        if request.user.role == 'volunteer':
            return obj.user == request.user
        

        return False