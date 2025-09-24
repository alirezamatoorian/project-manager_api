from django.contrib import admin
from .models import Project, Task


# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'manager', 'created_at']
    search_fields = ('title', 'members', 'manager')


admin.site.register(Task)
