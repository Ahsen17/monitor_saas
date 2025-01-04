import json
import redis
from common.meta import SingletonMeta
from configs.config import RedisConfig
from memsto.memsto import UnsafetyCache
from stats._base import Series, SeriesArray

from common.logger import debugLogger as logger


class _baseCollector(object):
    def collect(self):
        pass

    def stats(
            self,
            format_: str="",
            realTime: bool=False
        ) -> str:
        """
        :param format_: "prometheus", "opentsdb", etc.
        :param realTime: collect real-time stats or not
        """
        pass


class RedisCollector(
    _baseCollector,
    metaclass=SingletonMeta
):
    def __init__(self):
        _rConf = RedisConfig()

        self._cli = redis.Redis(
            host=_rConf.host,
            port=_rConf.port,
            password=_rConf.password,
            db=_rConf.database
        )

        self._rConf = _rConf

        self._mRedisConnState = "redis_connection_state"
        self._metrics = [
            self._mRedisConnState,
        ]

        self._stats = UnsafetyCache()
        self._descs = UnsafetyCache()
        
    def _collectConnState(self) -> Series:
        _metric = self._mRedisConnState

        # collect
        resp = self._cli.ping()
        state = 1 if resp else 0
        # storage
        self._stats.addEntry(_metric, Series(
            metric=_metric,
            value=state,
            tags={
                "host": self._rConf.host,
                "port": self._rConf.port,
            }
        ))
        self._descs.addEntry(_metric, ("Redis connection state.", "gauge"))

    def collect(self):
        self._collectConnState()

    def stats(self, format_: str="prometheus", realTime: bool=False) -> str:
        if realTime:
            self.collect()
        
        _res = SeriesArray(self._stats.getVals())
        _desc = {key: self._descs.getVal(key) for key in self._descs.getKeys()}

        if format_ == "prometheus":
            return _res.prometheus(description=_desc)
        elif format_ == "json":
            return json.dumps(_res.opentsdb())
        else:
            raise ValueError(f"Unsupported format: {format_}")
        

Collectors = [cls() for cls in _baseCollector.__subclasses__()]


def stats(format_="prometheus", realTime: bool=False) -> str:
    logger.debug(f"Collectors: {Collectors}")
    if format_ == "prometheus":
        return "\n".join([c.stats(format_, realTime) for c in Collectors])
    elif format_ == "opentsdb":
        _stats = []
        for instance in Collectors:
            _stats.append(json.loads(instance.stats(format_, realTime)))
        
        return json.dumps(_stats)
