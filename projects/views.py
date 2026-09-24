from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Project, Task, TaskComment, TaskActivity


@login_required
def dashboard(request):
    projects = Project.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    member_projects = Project.objects.filter(
        members=request.user
    ).exclude(
        owner=request.user
    ).order_by("-created_at")

    tasks = Task.objects.filter(
        assigned_to=request.user
    ).order_by("-created_at")

    total_projects = projects.count() + member_projects.count()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="completed").count()
    pending_tasks = tasks.exclude(status="completed").count()

    return render(
        request,
        "projects/dashboard.html",
        {
            "projects": projects,
            "member_projects": member_projects,
            "tasks": tasks,
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
        }
    )


@login_required
def create_project(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "planning")

        if name:
            project = Project.objects.create(
                name=name,
                description=description,
                status=status,
                owner=request.user
            )

            project.members.add(request.user)

            return redirect("dashboard")

    return render(request, "projects/create_project.html")


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id
    )

    if (
        project.owner != request.user
        and not project.members.filter(id=request.user.id).exists()
    ):
        return redirect("dashboard")

    tasks = project.tasks.all().order_by(
        "status",
        "-created_at"
    )

    members = project.members.all()

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
            "members": members,
        }
    )


@login_required
def create_task(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id
    )

    if (
        project.owner != request.user
        and not project.members.filter(id=request.user.id).exists()
    ):
        return redirect("dashboard")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        assigned_to_id = request.POST.get("assigned_to")
        status = request.POST.get("status", "todo")
        priority = request.POST.get("priority", "medium")
        due_date = request.POST.get("due_date")

        assigned_to = None

        if assigned_to_id:
            assigned_to = User.objects.filter(
                id=assigned_to_id
            ).first()

        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
            assigned_to=assigned_to,
            status=status,
            priority=priority,
            due_date=due_date if due_date else None
        )

        TaskActivity.objects.create(
            task=task,
            user=request.user,
            action=f"Created task '{task.title}'."
        )

        return redirect(
            "project_detail",
            project_id=project.id
        )

    members = project.members.all()

    return render(
        request,
        "projects/create_task.html",
        {
            "project": project,
            "members": members,
        }
    )


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id
    )

    project = task.project

    if (
        project.owner != request.user
        and task.assigned_to != request.user
    ):
        return redirect("dashboard")

    if request.method == "POST":
        task.title = request.POST.get(
            "title",
            task.title
        ).strip()

        task.description = request.POST.get(
            "description",
            task.description
        ).strip()

        task.status = request.POST.get(
            "status",
            task.status
        )

        task.priority = request.POST.get(
            "priority",
            task.priority
        )

        due_date = request.POST.get("due_date")
        task.due_date = due_date if due_date else None

        assigned_to_id = request.POST.get("assigned_to")

        if assigned_to_id:
            task.assigned_to = User.objects.filter(
                id=assigned_to_id
            ).first()
        else:
            task.assigned_to = None

        task.save()

        TaskActivity.objects.create(
            task=task,
            user=request.user,
            action=f"Updated task '{task.title}'."
        )

        return redirect(
            "project_detail",
            project_id=project.id
        )

    members = project.members.all()

    return render(
        request,
        "projects/edit_task.html",
        {
            "task": task,
            "project": project,
            "members": members,
        }
    )


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id
    )

    project_id = task.project.id

    if task.project.owner != request.user:
        return redirect("dashboard")

    if request.method == "POST":
        task.delete()

    return redirect(
        "project_detail",
        project_id=project_id
    )


@login_required
def add_comment(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == "POST":
        text = request.POST.get(
            "text",
            ""
        ).strip()

        if text:
            TaskComment.objects.create(
                task=task,
                user=request.user,
                text=text
            )

            TaskActivity.objects.create(
                task=task,
                user=request.user,
                action=f"Commented on task '{task.title}'."
            )

    return redirect(
        "project_detail",
        project_id=task.project.id
    )