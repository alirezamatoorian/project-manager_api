from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

app_name = 'project_manager'
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')

#nested router fot tasks
projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'tasks', views.TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
]
