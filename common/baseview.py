import http
import json
from django.http import HttpResponse
from django.views import View


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
        self._rawFlag = False

        super(ResourceViewMgr, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        
        self._META["HTTP_REQUEST"] = request
        self._META["METHOD"] = request.method
        self._META["QUERY_STRING"] = request.path

        return self._requestDistributes(*args, **kwargs)
    
    def resp(self, code=1001, status=False, data=None, message=""):
        self._result.update({k: v for k, v in locals().items() if k!= "self"})

    def respRaw(self, data: HttpResponse):
        assert isinstance(data, HttpResponse), TypeError("data must be an instance of HttpResponse.")
        self._result = data
        self._rawFlag = True
    
    def _requestDistributes(self, *args, **kwargs):
        """
        desc: http requset distributes: /api/${version}/${resource}/${operate}/${itemId}/
        """
        reqMethod = self._META["METHOD"]
        if reqMethod not in self._PERMITTED_METHODS:
            self.resp(code=CODE.METHOD_NOT_ALLOWED, message="Method not allowed.")
            return _response(**self._result)

        qStrs = [part for part in self._META['QUERY_STRING'].split('/') if part]
        if qStrs[0] != "api" or len(qStrs) < 4:
            self.resp(code=CODE.BAD_REQUEST)
            return _response(**self._result)
        
        version = qStrs[1]
        if version != self._VERSION:
            self.resp(code=CODE.BAD_REQUEST, message=f"Version [{version}] not supported.")
            return _response(**self._result)

        resource = qStrs[2]
        operate = qStrs[3]
        itemId = qStrs[4] if len(qStrs) > 4 else None

        if not hasattr(self, operate):
            self.resp(code=CODE.NOT_FOUND, message=f"[{operate}] not supported.")
            return _response(**self._result)
        
        try:
            _req = self._META['HTTP_REQUEST']
            self._META['PARAMS'] = json.loads(_req.body.decode()) if _req.body else _req.GET.dict()
            getattr(self, operate)(resource, itemId, *args, **kwargs)
        except Exception as e:
            self.resp(code=CODE.INTERNAL_SERVER_ERROR, message=str(e))
        return _response(**self._result) if not self._rawFlag else self._result

        
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
