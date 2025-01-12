import http
import json
import traceback
from django.http import HttpResponse
from django.views import View

from common.logger import djangoLogger as logger


CODE = http.HTTPStatus

STATUS = {
    CODE.OK: "success",
    CODE.BAD_REQUEST: "bad_request",
    CODE.METHOD_NOT_ALLOWED: "method_not_allowed",
    CODE.UNAUTHORIZED: "unauthorized",
    CODE.FORBIDDEN: "forbidden",
    CODE.NOT_FOUND: "not_found",
    CODE.INTERNAL_SERVER_ERROR: "server_error",
}

class _response(object):
    def __new__(cls, *args, **kwargs):
        res = kwargs
        res['message'] = res.get("message") or STATUS.get(res.get("code", 1001), "Unknown error.")
        return HttpResponse(json.dumps(args or kwargs), content_type="application/json")


class ResourceViewMgr(View):
    _VERSION = "v1"
    _PERMITTED_METHODS = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self, *args, **kwargs):

        self._META = {
            "HTTP_REQUEST": None,
            "METHOD": "",
            "QUERY_STRING": "",
            "PARAMS": {},
        }

        self._result = {}
        self._rawResp = False

        super(ResourceViewMgr, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        assert request.method in self._PERMITTED_METHODS, "Method not allowed."
        
        self._META["HTTP_REQUEST"] = request
        self._META["QUERY_STRING"] = request.path

        self._requestDistributes(*args, **kwargs)
        return self._result if self._rawResp else _response(**self._result)
    
    def resp(self, code=1001, status=False, data=None, message=""):
        self._result.update({k: v for k, v in locals().items() if not k.startswith("self")})

    def respRaw(self, data: HttpResponse):
        assert isinstance(data, HttpResponse), TypeError("Data must be an instance of HttpResponse.")
        self._result = data
        self._rawResp = True
    
    def _requestDistributes(self, *args, **kwargs):
        """
        desc: http requset distributes: /api/${version}/${resource}/${operate}/${itemId}/
        """
        qStrs = [part for part in self._META['QUERY_STRING'].split('/') if part]
        if qStrs[0] != "api" or len(qStrs) < 4 or qStrs[1] != self._VERSION:
            raise NotImplementedError("Invalid request path.")
        
        version = qStrs[1]
        resource = qStrs[2]
        operate = qStrs[3]
        itemId = qStrs[4] if len(qStrs) > 4 else None

        if not hasattr(self, operate):
            return self.resp(code=CODE.NOT_FOUND, message=f"Operation [{operate}] not supported.")
        
        try:
            _req = self._META['HTTP_REQUEST']
            self._META['PARAMS'] = json.loads(_req.body.decode()) if _req.body else _req.GET.dict()
            getattr(self, operate)(resource, itemId, *args, **kwargs)
        except Exception as e:
            logger.error(f"{str(e)} \n {traceback.exec_format()}")
            self.resp(code=CODE.INTERNAL_SERVER_ERROR, message=str(e))

        
class ResourceViewMgrV2(ResourceViewMgr):
    _VERSION = "v2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _requestDistributes(self, *args, **kwargs):
        # TODO: v2 new features
        pass


# TODO: v3 add django rest_framework
class ResourceViewMgrV3:
    pass
