import json
import os
from django.http import HttpResponse

from configs.settings import BASE_DIR, CONFIGS
from common.logger import djangoLogger as logger
from common.baseview import CODE, ResourceViewMgr

# Create your views here.

def version(request):
    with open(os.path.join(BASE_DIR, "VERSION"), "r") as f:
        version = f.read().strip()
    return HttpResponse(content=version)


def info(request):
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(CONFIGS.all())
    )


def metrics(request):
    return HttpResponse("Welcome to SysStat Metrics!")
