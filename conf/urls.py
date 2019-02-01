"""zt_dd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', include('apps.web.urls')),
    path('api/', get_schema_view()),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/portfolios/', include('apps.portfolio.urls')),
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api/', include('apps.rest_api.urls')),
    # url(r'^api/$', get_schema_view()),
    # url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    # url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
    # # React App Entry
    # url(r'^', TemplateView.as_view(template_name="index.html")),
]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
