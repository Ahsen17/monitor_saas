from django.http import HttpResponse


# Create your views here.

def TestIterator(req):
    from memsto.memsto_test import TestCacheIterator as tci
    tci()
    return HttpResponse("TestIterator")