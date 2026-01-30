from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    path('export/tasks/', views.ExportTasksCSV.as_view(), name='export_tasks_csv'),
]
