from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .permissions import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from .pagination import CustomPagination
from django.db.models import Q


# Create your views here.


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().select_related('manager').prefetch_related('members')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]

    @action(methods=['post'], detail=True, permission_classes=[IsOwner])
    def add_member_to_project(self, request, pk=None):
        project = self.get_object()
        user_phone = request.data.get('user_phone')
        if not user_phone:
            return Response({"error": "user_phone is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, phone=user_phone)
        project.members.add(user)
        return Response({"status": f"{user.phone} added to project"}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=[IsOwner])
    def remove_member_from_project(self, request, pk=None):
        project = self.get_object()
        user_phone = request.data.get('user_phone')
        if not user_phone:
            return Response({"error": "user_phone is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, phone=user_phone)
        if user == project.manager:
            return Response({"error": "مدیر پروژه نمی‌تواند حذف شود"}, status=status.HTTP_400_BAD_REQUEST)
        if not project.members.filter(phone=user_phone).exists():
            return Response({"error": "این کاربر عضو پروژه نیست"}, status=status.HTTP_400_BAD_REQUEST)
        project.members.remove(user)
        return Response({"status": f"{user.phone} remove from project"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "پروژه با موفقیت ساخته شد",
            "project": response.data
        }
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        return Task.objects.filter(
            Q(project__members=self.request.user) | Q(pproject__manager=self.request.user)) \
            .select_related('project', 'assignee')

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, id=project_id)

        if self.request.user != project.manager:
            raise PermissionDenied("فقط مدیر پروژه می‌تواند تسک بسازد.")

        assigned_to = self.request.data.get("assignee")
        if assigned_to and not project.members.filter(id=assigned_to).exists():
            raise ValidationError("این کاربر عضو پروژه نیست.")

        serializer.save(project=project)
