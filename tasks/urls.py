from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/update/<int:pk>/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/delete/<int:pk>/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/update/<int:pk>/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task_delete'),
]
