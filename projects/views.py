# ==========================================
# 11. projects/views.py
# ==========================================
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project
from .serializers import ProjectSerializer
from accounts.permissions import IsManager

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsManager]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'manager':
            return Project.objects.all()
        return Project.objects.filter(team_members=user)
    
    @action(detail=False, methods=['get'])
    def my_projects(self, request):
        projects = Project.objects.filter(team_members=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


@login_required
def projects_view(request):
    if request.user.role in ['admin', 'manager']:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(team_members=request.user)
    
    return render(request, 'projects.html', {'projects': projects})

