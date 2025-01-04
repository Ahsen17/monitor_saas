from django.urls import path, re_path

from stats import views as ssViews

urlpatterns = [
    path('metrics/', ssViews.metrics, name='metrics'),
    
    path('api/v1/system/configs/', ssViews.SystemConfigsView.as_view(), name='system_configs'),
]