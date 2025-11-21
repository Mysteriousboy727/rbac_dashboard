# rbac_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts.views import login_view, logout_view, dashboard_view, profile_view, users_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('accounts.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/reports/', include('reports.urls')),
    
    # Template views (HTML pages)
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('users/', users_view, name='users'),
    
    # ADD THESE LINES:
    path('projects/', TemplateView.as_view(template_name='projects.html'), name='projects'),
    path('tasks/', TemplateView.as_view(template_name='tasks.html'), name='tasks'),
    
    # API root (from REST framework router)
    path('', include('accounts.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)