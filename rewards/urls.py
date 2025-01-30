from django.urls import path
from .views import (
    RegisterAPI, LoginAPI,
    AppListCreateAPI, TaskListCreateAPI,
    UserProfileAPI, TaskApproveAPI
)

urlpatterns = [
    # Authentication
    path('register/', RegisterAPI.as_view(), name='api_register'),
    path('login/', LoginAPI.as_view(), name='api_login'),
    
    # Apps & Tasks
    path('apps/', AppListCreateAPI.as_view(), name='api_apps'),
    path('tasks/', TaskListCreateAPI.as_view(), name='api_tasks'),
    path('api/tasks/<int:pk>/approve/', TaskApproveAPI.as_view(), name='task-approve'),
    
    # User Profile
    path('profile/', UserProfileAPI.as_view(), name='api_profile'),
]