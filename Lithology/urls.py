"""Lithology URL Configuration

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
from re import template
from django.contrib import admin
from django.urls import path
# from django.conf.urls import url
from backend import views,discontinuity_detection
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='homepage'),
    path('predictComposition',views.predictComposition,name='predictImage'),
    path('predict_discontinuities',discontinuity_detection.predict_discontinuities,name='predictImage'),
    path('dashboard',views.dashboard,name='dashboard'),
    path("chatbot",views.chatbot)
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)