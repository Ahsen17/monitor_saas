from django.urls import path, re_path

from stats import views as ssViews

from tests import views as tsViews

urlpatterns = [
    path('metrics/', ssViews.metrics, name='metrics'),
    
    path('system/version/', ssViews.version, name='version'),

    path('api/v1/cache/test/', tsViews.UnsafetyCacheExam.as_view(), name='test_cache_unsafety'),
    path('api/v1/segment/test/', tsViews.MultiSegmentsSafetyCacheExam.as_view(), name='test_cache_multi_segments'),
]