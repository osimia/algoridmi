"""
URL configuration for al_khwarizmi project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/user/', include('users.urls')),
    path('api/problems/', include('problems.urls')),
    path('api/arena/', include('arena.urls')),
    
    # Frontend - serve index.html for all other routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Администрация Ал Хоразми"
admin.site.site_title = "Ал Хоразми Admin"
admin.site.index_title = "Добро пожаловать в панель управления"
