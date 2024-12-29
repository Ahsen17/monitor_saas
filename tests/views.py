from django.shortcuts import render

from common.baseview import ResourceViewMgr
from memsto.memsto_test import TestMultiSegmentSafetyCache, TestUnsafetyCache

# Create your views here.

class UnsafetyCacheExam(ResourceViewMgr):
    def test(self, resource: str, itemId: str):
        TestUnsafetyCache()
        self.resp(code=200, status=True, message="success")

    
class MultiSegmentsSafetyCacheExam(ResourceViewMgr):
    def test(self, resource: str, itemId: str):
        TestMultiSegmentSafetyCache()
        self.resp(code=200, status=True, message="success")