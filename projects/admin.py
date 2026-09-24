from django.contrib import admin
from .models import Project, Task, TaskComment, TaskActivity


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__username")
    filter_horizontal = ("members",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "assigned_to",
        "status",
        "priority",
        "due_date",
        "created_at",
    )
    list_filter = (
        "status",
        "priority",
        "due_date",
    )
    search_fields = (
        "title",
        "description",
        "project__name",
        "assigned_to__username",
    )


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "user",
        "text",
        "created_at",
    )
    search_fields = (
        "task__title",
        "user__username",
        "text",
    )


@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "user",
        "action",
        "created_at",
    )
    search_fields = (
        "task__title",
        "user__username",
        "action",
    )
    