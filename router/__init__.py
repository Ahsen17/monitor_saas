from typing import Any, Callable, Dict, List, Text, Tuple

from django.http import HttpResponse
from django.urls import URLPattern, path, re_path

ViewType = Callable[..., HttpResponse]


class UrlPatterns(object):
    def __init__(self):
        self._group = ()
        self._routes = []
        self._regexs = []

    def group(self, *path: str) -> "UrlPatterns":
        self._group = path

        return self

    def registry(
        self,
        route: str,
        view: ViewType,
        kwargs: Dict[str, Any]=...,
        name: str=...,
        onRegex: bool=False
    ) -> "UrlPatterns":
        if kwargs == ...: kwargs = {}
        params = (route, view, kwargs, name)

        if not onRegex:
            self._routes.append(params)
        else:
            self._regexs.append(params)
        
        return self

    def routes(self) -> List[URLPattern]:
        _routes = [
            path("/".join(list(self._group) + [route[0]]), *route[1:])
            for route in self._routes if route
        ]
        _regexs = [
            re_path("/".join(list(self._group) + [regex[0]]), *regex[1:])
            for regex in self._regexs if regex
        ]

        return _routes + _regexs