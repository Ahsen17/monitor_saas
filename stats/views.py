import gzip
import os
from django.http import HttpResponse

from configs.config import BASE_DIR, CONFIGS
from common.logger import djangoLogger as logger
from stats.utils import stats

# Create your views here.

def version(request):
    with open(os.path.join(BASE_DIR, "VERSION"), "r") as f:
        version = f.read().strip()
    return HttpResponse(content=version)


def metrics(request):
    _stats = stats(format_="prometheus", realTime=True)
    # return gzip compressed response
    response = HttpResponse(
        content=gzip.compress(_stats.encode("utf-8")),
        content_type="text/plain"
    )
    response["Content-Encoding"] = "gzip"
    return response
