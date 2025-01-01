import json


class _baseCollector(object):
    def collect(self):
        pass

    def stats(
            self,
            format_="prometheus",
            realTime: bool=False
        ) -> str:
        """
        :param format_: supported formats: "prometheus", "opentsdb"
        :param realTime: collect real-time stats or not
        """
        pass


# TODO: comes a bug, cannot generate collector instances
Collectors = [_cls() for _cls in _baseCollector.__subclasses__()]


def stats(format_="prometheus", realTime: bool=False) -> str:
    if format_ == "prometheus":
        return "\n".join([c.stats(format_, realTime) for c in Collectors])
    elif format_ == "opentsdb":
        _stats = []
        for instance in Collectors:
            _stats.append(json.loads(instance.stats(format_, realTime)))
        
        return json.dumps(_stats)