from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("project/create/", views.create_project, name="create_project"),
    path("project/<int:project_id>/", views.project_detail, name="project_detail"),
    path("project/<int:project_id>/task/create/", views.create_task, name="create_task"),
    path("task/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("task/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("task/<int:task_id>/comment/", views.add_comment, name="add_comment"),
]