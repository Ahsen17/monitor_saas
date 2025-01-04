from django.urls import path, re_path

from tests import views as tw

urlpatterns = [
    path('test/iterator/', tw.TestIterator, name='test_iterator'),
]