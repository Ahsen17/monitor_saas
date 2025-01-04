"""
@Time    : Wed Dec 25 01:11 CST 2024
@Author  : ahsen
@Email   : ahsenedward@gmail.com
@File    : _base.py

This module defines the base classes for metrics and metrics collection.

OpenTSDB:
[
    {
        "metric": "sys.cpu.user",
        "value": 10.0,
        "tags": {
            "host": "web01",
        }
    }
]

Prometheus:
# HELP sys_cpu_user System CPU utilization
# TYPE sys_cpu_user gauge
sys_cpu_user{host="web01",instance="localhost:9090"} 10.0
"""


from enum import Enum
import json
from typing import Any, Dict, List, Tuple, Union


class SeriesTypeEnum(Enum):
    GAUGE = "gauge"
    COUNTER = "counter"
    SUMMARY = "summary"
    HISTOGRAM = "histogram"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
    
    @classmethod
    def values(cls):
        return list(cls._value2member_map_.keys())
    
    @classmethod
    def names(cls):
        return list(cls._value2member_map_.values())


class Series(object):
    def __init__(self, metric: str, value: Union[int, float], tags: dict):
        self.metric = metric
        self.value = value
        self.tags = tags
    
    @classmethod
    def load(cls, data: Dict[str, Any]) -> "Series":
        return cls(data["metric"], data["value"], data["tags"])
    

class SeriesArray(object):
    def __init__(self, metrics: List[Series]=[]):
        self._metrics = metrics

    def append(self, metric: Series):
        self._metrics.append(metric)

    def extend(self, metrics: List[Series]):
        self._metrics.extend(metrics)

    def opentsdb(self) -> str:
        return json.dumps([{
            "metric": m.metric,
            "value": m.value,
            "tags": m.tags
        } for m in self._metrics])
    
    def prometheus(
        self,
        description: Dict[str, Tuple[str, str]] = {}
    ) -> str:
        """
        :param description:
            {"metric": ("# HELP", "# TYPE")}
        """
        _mCache = {}
        for metric in self._metrics:
            if metric.metric not in _mCache:
                _mCache[metric.metric] = []
            _mCache[metric.metric].append(metric)
        
        _content = ""
        for _metric, _seriesLst in _mCache.items():
            help, type_ = description.get(metric.metric, ("No description of metric.", SeriesTypeEnum.GAUGE.value))
            _content += f"# HELP {_metric} {help} \n"
            _content += f"# TYPE {_metric} {type_}\n"
            for series in _seriesLst:
                tags = ",".join([f'{k}="{v}"' for k, v in series.tags.items()])
                _content += f"{series.metric}{{{tags}}} {series.value}\n"

        return _content

    @classmethod
    def _loadPrometheus(cls, content: str) -> "SeriesArray":
        _lines = content.split("\n")
        _seriesArr = []

        # for example:
        # cpu_usage{ident="0",tags="a,b,c"} 0.1
        # translate prometheus to opentsdb format
        for line in _lines:
            if line.startswith("#"):
                continue
            series, value = line.split(" ")
            metric = series.split("{")[0]
            _tagsLine = series.split("{")[1].split("}")[0]
            if '{' in _tagsLine and '}' in _tagsLine:
                tags = _tagsLine.split('{')[1].split('}')[0]
            else:
                tags = ''
            
            p, flag = 0, False
            keyLst, valLst = [], []
            for idx, c in enumerate(tags):
                if idx < p: continue
                if p >= len(tags): break
                if c == '=':
                    keyLst.append(tags[p:idx])
                    p = idx + 1
                    continue
                if c == '"':
                    if not flag:
                        p = idx + 1
                        flag = True
                        continue
                    else:
                        valLst.append(tags[p:idx])
                        p = idx + 2
                        flag = False
                        continue
            
            tags = {k: v for k,v in zip(keyLst, valLst)}
            
            _seriesArr.append(Series(metric, float(value), tags))

        return cls(_seriesArr)

    @classmethod
    def _loadOpentsdb(cls, content: List[Dict]) -> "SeriesArray":
        _seriesArr = []
        for _metric in content:
            _seriesArr.append(Series.load(_metric))

        return cls(_seriesArr)
    
    @classmethod
    def load(cls, content: Union[str, List], format_: str) -> "SeriesArray":
        """
        Load metrics from different formats.
        Args:
            content: the content of metrics, can be a string or a list of dict.
            format: the format of metrics, can be "prometheus" or "opentsdb".
        Returns:
            A Metrics object.
        Raises:
            ValueError: if the format is not supported.
        """
        if format_ == "prometheus":
            return cls._loadPrometheus(content)
        elif format_ == "opentsdb":
            return cls._loadOpentsdb(content)
        else:
            raise ValueError(f"Unsupported format: {format}")
        