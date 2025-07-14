from django.urls import path
from .views import (
    RoleListCreateView, RoleDetailView,
    PermissionListCreateView, PermissionDetailView,
    UserListCreateView, UserDetailView
)

urlpatterns = [
    path('roles/', RoleListCreateView.as_view()),
    path('roles/<int:pk>/', RoleDetailView.as_view()),
    path('permissions/', PermissionListCreateView.as_view()),
    path('permissions/<int:pk>/', PermissionDetailView.as_view()),
    path('users/', UserListCreateView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
]
