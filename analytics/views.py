from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from tasks.models import Task, Project
from accounts.models import User
import pandas as pd
import json
import csv

class AdminManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['admin', 'manager']

class AnalyticsDashboardView(LoginRequiredMixin, AdminManagerRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Tasks Data
        tasks = Task.objects.all().values('id', 'title', 'status', 'priority', 'deadline', 'assigned_to__username')
        df_tasks = pd.DataFrame(list(tasks))
        
        # Projects Data
        projects = Project.objects.all().values('id', 'name', 'status', 'start_date', 'end_date')
        df_projects = pd.DataFrame(list(projects))

        if not df_tasks.empty:
            # Status Counts
            status_counts = df_tasks['status'].value_counts().to_dict()
            context['task_status_labels'] = list(status_counts.keys())
            context['task_status_data'] = list(status_counts.values())

            # Priority Counts
            priority_counts = df_tasks['priority'].value_counts().to_dict()
            context['task_priority_labels'] = list(priority_counts.keys())
            context['task_priority_data'] = list(priority_counts.values())

            # KPIs
            context['total_tasks'] = len(df_tasks)
            context['completed_tasks'] = len(df_tasks[df_tasks['status'] == 'completed'])
            context['pending_tasks'] = len(df_tasks[df_tasks['status'] == 'pending'])
        else:
            context['total_tasks'] = 0
            context['completed_tasks'] = 0
            context['pending_tasks'] = 0

        if not df_projects.empty:
            context['total_projects'] = len(df_projects)
            context['active_projects'] = len(df_projects[df_projects['status'] == 'active'])
        else:
            context['total_projects'] = 0
            context['active_projects'] = 0

        # AI Suggestions
        from .ai import get_ai_suggestions
        context['ai_suggestions'] = get_ai_suggestions(self.request.user)

        return context

class ExportTasksCSV(LoginRequiredMixin, AdminManagerRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Title', 'Project', 'Assigned To', 'Priority', 'Status', 'Deadline'])
        
        tasks = Task.objects.select_related('project', 'assigned_to').all()
        for task in tasks:
            writer.writerow([task.title, task.project.name, task.assigned_to.username if task.assigned_to else 'Unassigned', task.priority, task.status, task.deadline])
            
        return response
