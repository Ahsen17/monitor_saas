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
from typing import Any, Dict, List, Tuple


class MetricTypeEnum(Enum):
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


class Metric(object):
    def __init__(self, metric: str, value: float, tags: dict):
        self.metric = metric
        self.value = value
        self.tags = tags
    
    def __dict__(self):
        return {
            "metric": self.metric,
            "value": self.value,
            "tags": self.tags
        }
    
    @classmethod
    def load(cls, data: Dict[str, Any]) -> "Metric":
        return cls(data["metric"], data["value"], data["tags"])
    

class Metrics(object):
    def __init__(self, metrics: List[Metric]):
        self.metrics = metrics

    def opentsdb(self) -> List[Dict[str, Any]]:
        return [m.__dict__() for m in self.metrics]
    
    def prometheus(
        self,
        description: Dict[str, Tuple[str, str]] = {}
    ) -> str:
        _mCache = {}
        for metric in self.metrics:
            if metric.metric not in _mCache:
                _mCache[metric.metric] = []
            _mCache[metric.metric].append(metric)
        
        _content = ""
        for _metric, _seriesLst in _mCache.items():
            _help, _type = description.get(metric.metric, ("No description of metric.", "gauge"))
            _content += f"# HELP {_metric} {_help} \n"
            _content += f"# TYPE {_metric} {_type}\n"
            for _series in _seriesLst:
                _tags = ",".join([f'{k}="{v}"' for k, v in _series.tags.items()])
                _content += f"{_series.metric}{{{_tags}}} {_series.value}\n"

        return _content

    @classmethod
    def _loadPrometheus(cls, content: str) -> "Metrics":
        _lines = content.split("\n")
        _metrics = []

        # for example:
        # cpu_usage{ident="0",tags="a,b,c"} 0.1
        # translate prometheus to opentsdb format
        for line in _lines:
            if line.startswith("#"):
                continue
            _series, _value = line.split(" ")
            _metric = _series.split("{")[0]
            _tagsLine = _series.split("{")[1].split("}")[0]
            _tagKeys = []
            _tagVals = []
            for _tag in _tagsLine.split("="):
                # TODO: comes a bug, generate new tags which are not needed.
                _tagKeys.append(_tag.split(",")[-1])
                _tagVals.append(_tag[_tag.find('"')+1:_tag.rfind('"')])
            _tags = dict(zip(_tagKeys, _tagVals))
            _metrics.append(Metric(_metric, float(_value), _tags))

        return cls(_metrics)

    @classmethod
    def _loadOpentsdb(cls, content: List[dict]) -> "Metrics":
        _metrics = []
        for _metric in content:
            _metrics.append(Metric.load(_metric))

        return cls(_metrics)
    
    @classmethod
    def load(cls, content: Any, format: str) -> "Metrics":
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
        if format == "prometheus":
            return cls._loadPrometheus(content)
        elif format == "opentsdb":
            return cls._loadOpentsdb(content)
        else:
            raise ValueError(f"Unsupported format: {format}")
        