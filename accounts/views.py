# ==========================================
# 6. accounts/views.py
# ==========================================
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import AuditLog
from .serializers import UserSerializer, AuditLogSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin
import csv
from django.http import HttpResponse

User = get_user_model()


# API Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        AuditLog.objects.create(user=user, action='Login', details='API Login')
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Username', 'Email', 'Role', 'First Name', 'Last Name', 'Created At'])
        
        users = User.objects.all()
        for user in users:
            writer.writerow([user.id, user.username, user.email, user.role, 
                           user.first_name, user.last_name, user.created_at])
        
        return response


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]


# Template Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            auth_login(request, user)
            AuditLog.objects.create(user=user, action='Login', details='Web Login')
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    context = {
        'user': request.user,
        'total_users': User.objects.count() if request.user.is_admin else None,
        'total_projects': None,  # Will be filled by projects app
        'total_tasks': None,  # Will be filled by tasks app
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.bio = request.POST.get('bio', user.bio)
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        AuditLog.objects.create(user=user, action='Profile Updated')
        return redirect('profile')
    
    return render(request, 'profile.html', {'user': request.user})


@login_required
def users_view(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


@login_required
def logout_view(request):
    AuditLog.objects.create(user=request.user, action='Logout')
    auth_logout(request)
    return redirect('login')

