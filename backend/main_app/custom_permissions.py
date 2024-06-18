from rest_framework.permissions import  BasePermission


class IsAdminOrOwnerPermission(BasePermission):
    """
    Пользовательский класс разрешения, позволяющий доступ только администраторам
    или владельцам объектов.
    """

    def has_permission(self , request , view):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated

    def has_object_permission(self , request , view , obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user