# ==========================================
# 12. projects/urls.py
# ==========================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ProjectViewSet, basename='project')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.projects_view, name='projects'),
]