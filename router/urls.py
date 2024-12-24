from django.urls import path, re_path

from stats import views as ssViews

urlpatterns = [
    path('metrics/', ssViews.metrics, name='metrics'),
    path('system/version/', ssViews.version, name='version'),
    path('system/info/', ssViews.info, name='system_info'),
]