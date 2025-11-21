# ==========================================
# 15. tasks/serializers.py
# ==========================================
from rest_framework import serializers
from .models import Task
from accounts.serializers import UserSerializer
from projects.serializers import ProjectSerializer

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True)
    project_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'