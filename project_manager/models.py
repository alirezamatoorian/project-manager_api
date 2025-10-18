from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        ARCHIVE = 'archive', 'Archive'

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', db_index=True)
    members = models.ManyToManyField(User, related_name="member_projects")
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Task(models.Model):
    class Status(models.TextChoices):
        Todo = "todo", "Todo"
        IN_PROGRESS = "in progress", "In_progress"
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='tasks_file/', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=11, choices=Status.choices, default=Status.Todo)
    priority = models.CharField(max_length=11, choices=Priority.choices, default=Priority.LOW)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # فرد مسئول

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
