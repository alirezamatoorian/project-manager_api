from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email']


class ProjectSerializer(serializers.ModelSerializer):
    manager = UserMiniSerializer(read_only=True)
    members = UserMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'manager', 'members']
        read_only_fields = ['members', 'manager']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assignee', 'created_at', 'status', 'priority']
        read_only_fields = ['id', 'created_at', 'status', 'priority']
