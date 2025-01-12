import gzip
import json
import os
from django.http import HttpResponse

from common.baseView import CODE, ResourceViewMgr
from configs.config import BASE_DIR, CONFIGS
from common.logger import djangoLogger as logger
from stats.utils.collectors import stats

# Create your views here.

def metrics(request):
    _stats = stats(format_="prometheus", realTime=True)
    # return gzip compressed response
    response = HttpResponse(
        content=gzip.compress(_stats.encode("utf-8")),
        content_type="text/plain"
    )
    response["Content-Encoding"] = "gzip"
    return response


class SystemConfigsView(ResourceViewMgr):
    def _version(self) -> str:
        try:
            with open(os.path.join(BASE_DIR, "VERSION"), "r") as f:
                version = f.read().strip()
            return version
        except:
            return "unknown"

    def configs(self, resource=None, itemId=None):
        _configs = {
            "version": self._version(),
        }

        # self.resp(code=CODE.OK, status=True, data=_configs)
        self.respRaw(HttpResponse(
            content=json.dumps(_configs), 
            content_type="application/json"
        ))
