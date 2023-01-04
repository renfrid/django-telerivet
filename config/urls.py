"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from apps.api import views as api_views
from apps.api import utils

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.account.urls')),
    path('accounts/', include('apps.account.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('setup/', include('apps.menu.urls')),
    path('citizens/', include('apps.citizen.urls')),
    path('leaders/', include('apps.leader.urls')),
    path('location/', include('apps.location.urls')),

    #apis
    path('webhooks/telerivet/', api_views.webhook),
    path('wards/', utils.get_wards),
    path('villages/', utils.get_villages),
]
