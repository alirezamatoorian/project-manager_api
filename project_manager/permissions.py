from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.manager == request.user or request.user == request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.manager == request.user


class IsProjectMember(BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')
        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                return False

            if request.user == project.manager:
                return True
            if request.method in SAFE_METHODS and request.user in project.members.all():
                return True
            return False

        return True  # در بقیه حالت‌ها اجازه بدیم بره به has_object_permission

    def has_object_permission(self, request, view, obj):
        if request.user == obj.project.manager:
            return True
        if request.method in SAFE_METHODS and request.user in obj.project.members.all():
            return True
        return False
