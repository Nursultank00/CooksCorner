"""
URL configuration for cookscorner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
   openapi.Info(
      title="CooksCorner",
      default_version='v1.0',
       description="Проект предоставляет доступ к запросам, связанных с приложением для сообщества кулинаров.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="auth.project.nursultan@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    re_path(r'^cookscorner/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^cookscorner/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^cookscorner/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('cookscorner/admin/', admin.site.urls),
    path('cookscorner/users/', include('users.urls')),
    path('cookscorner/profile/', include('userprofile.urls')),
    path('cookscorner/receipts/', include('receipts.urls')),
]
