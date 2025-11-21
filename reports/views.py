# ==========================================
# 19. reports/views.py
# ==========================================
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.permissions import IsAdmin
from projects.models import Project
from tasks.models import Task

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdmin])
def dashboard_stats(request):
    stats = {
        'total_users': User.objects.count(),
        'total_projects': Project.objects.count(),
        'total_tasks': Task.objects.count(),
        'active_projects': Project.objects.filter(status='active').count(),
        'completed_tasks': Task.objects.filter(status='done').count(),
        'pending_tasks': Task.objects.filter(status='todo').count(),
        'in_progress_tasks': Task.objects.filter(status='in_progress').count(),
        'users_by_role': {
            'admin': User.objects.filter(role='admin').count(),
            'manager': User.objects.filter(role='manager').count(),
            'user': User.objects.filter(role='user').count(),
        }
    }
    return Response(stats)


