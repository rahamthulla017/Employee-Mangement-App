from django.urls import path
from . import views

urlpatterns = [
    path('api/get/', views.get_notifications, name='get_notifications'),
    path('api/read/<int:pk>/', views.mark_read, name='mark_notification_read'),
    path('', views.notification_list, name='notification_list'),
]
