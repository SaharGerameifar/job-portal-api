from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    The request is owner as a user , or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and obj.user == request.user
        )


class IsEmployeeOwnerOrReadOnly(BasePermission):
    """
    The request is employee owner as a user , or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and obj.employee.user == request.user
        )


class IsCompanyOwnerOrReadOnly(BasePermission):
    """
    The request is company owner as a user , or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and obj.company.user == request.user
        )


class IsJobCompanyOwnerOrReadOnly(BasePermission):
    """
    The request is job company owner as a user , or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and obj.job.company.user == request.user
        )


class IsCompanyOrReadOnly(BasePermission):
    """
    The request is a company , or is a read-only request.
    """

    def has_permission(self, request, view):
        
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and request.user.role == 'C'
        )

       
class  IsEmployeeOrReadOnly(BasePermission):
    """
    The request is a employee , or is a read-only request.
    """

    def has_permission(self, request, view):
        
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and request.user.role == 'E'
        )
