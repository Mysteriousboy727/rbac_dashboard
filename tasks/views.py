# ==========================================
# 16. tasks/views.py
# ==========================================
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
from .serializers import TaskSerializer
from accounts.permissions import IsManager

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsManager()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


@login_required
def tasks_view(request):
    if request.user.role in ['admin', 'manager']:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)
    
    return render(request, 'tasks.html', {'tasks': tasks})

