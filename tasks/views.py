from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Project, Task
from accounts.models import User
from .forms import ProjectForm, TaskForm
from notifications.models import Notification

class AdminManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['admin', 'manager']

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'

class ProjectCreateView(LoginRequiredMixin, AdminManagerRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Project created successfully.")
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, AdminManagerRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_form.html'
    success_url = reverse_lazy('project_list')

class ProjectDeleteView(LoginRequiredMixin, AdminManagerRequiredMixin, DeleteView):
    model = Project
    template_name = 'tasks/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Employees see only their tasks or tasks in their projects?
        # Prompt says "Employees can update tasks".
        user = self.request.user
        if user.role == 'employee':
            return Task.objects.filter(assigned_to=user)
        return Task.objects.all()

class TaskCreateView(LoginRequiredMixin, AdminManagerRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        task = self.object
        if task.assigned_to:
            Notification.objects.create(
                user=task.assigned_to,
                message=f"You have been assigned a new task: {task.title}"
            )
        messages.success(self.request, "Task created and assigned.")
        return response

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role == 'employee':
            # Employees can only update status
            for field in form.fields:
                if field != 'status':
                    form.fields[field].disabled = True
        return form

    def form_valid(self, form):
        if form.has_changed():
             # Notify managers about update
             task = self.object
             managers = User.objects.filter(role__in=['admin', 'manager'])
             for manager in managers:
                 Notification.objects.create(
                     user=manager,
                     message=f"Task '{task.title}' updated by {self.request.user.username}."
                 )
        messages.success(self.request, "Task updated.")
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, AdminManagerRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
