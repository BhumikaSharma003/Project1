# rewards/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from .models import *
from .permissions import IsAdminUser

# API Views
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        auth_login(request, user)  # Create session for template views
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class AppListCreateAPI(generics.ListCreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        # Allow any authenticated user to view apps
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        # Only admins can create new apps
        return [permissions.IsAuthenticated(), IsAdminUser()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user, status='pending')
        task.status = 'approved'
        task.save()
        
        # Update user profile
        profile = self.request.user.userprofile
        profile.points_earned += task.app.points
        profile.tasks_completed += 1
        profile.save()

class UserProfileAPI(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

class TaskApproveAPI(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        task = serializer.save(status='approved')
        profile = task.user.userprofile
        profile.points_earned += task.app.points
        profile.tasks_completed += 1
        profile.save()

# Frontend Views

def home(request):
    return render(request, 'rewards/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # Handle form submission through API
        return redirect('login')  # Redirect after successful registration
    
    return render(request, 'rewards/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'rewards/login.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_admin:
        return redirect('admin_dashboard')
    return render(request, 'rewards/profile.html')

def apps_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'rewards/apps.html')

def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('home')
    return render(request, 'rewards/admin_dashboard.html')

def logout_view(request):
    if request.user.is_authenticated:
        request.auth.delete() if hasattr(request, 'auth') else None
        request.session.flush()
    return redirect('home')