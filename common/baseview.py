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

    _PERMITTED_METHODS = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self, *args, **kwargs):

        self._META = {
            "HTTP_REQUEST": None,
            "METHOD": "",
            "QUERY_STRING": "",
        }

        self._result = {}

        self.version = "v1"

        super(ResourceViewMgr, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        
        self._META["HTTP_REQUEST"] = request
        self._META["METHOD"] = request.method
        self._META["QUERY_STRING"] = request.path

        return self._requestDistributes(request.path, *args, **kwargs)
    
    def resp(self, code=1001, status=False, data=None, message=""):
        self._result.update({k: v for k, v in locals().items() if k!= "self"})
    
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
        resource = qStrs[2]
        operate = qStrs[3]
        itemId = qStrs[4] if len(qStrs) > 4 else None

        if not hasattr(self, operate):
            self.resp(code=CODE.NOT_FOUND, message=f"[{operate}] not supported.")
            return _response(**self._result)
        
        try:
            getattr(self, operate)(resource, itemId, *args, **kwargs)
        except Exception as e:
            self.resp(code=CODE.INTERNAL_SERVER_ERROR, message=str(e))
        return _response(**self._result)

        

