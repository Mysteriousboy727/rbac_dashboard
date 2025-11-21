# ==========================================
# 10. projects/serializers.py
# ==========================================
from rest_framework import serializers
from .models import Project
from accounts.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    team_members = UserSerializer(many=True, read_only=True)
    team_member_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def create(self, validated_data):
        team_member_ids = validated_data.pop('team_member_ids', [])
        project = Project.objects.create(**validated_data)
        if team_member_ids:
            project.team_members.set(team_member_ids)
        return project
    
    def update(self, instance, validated_data):
        team_member_ids = validated_data.pop('team_member_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if team_member_ids is not None:
            instance.team_members.set(team_member_ids)
        return instance

