import json
import redis
from configs.config import RedisConfig
from stats._base import Series, SeriesArray
from stats.utils import _baseCollector


class RedisCollector(_baseCollector):
    def __init__(self):
        _rConf = RedisConfig()

        self._cli = redis.Redis(
            host=_rConf.host,
            port=_rConf.port,
            password=_rConf.password,
            db=_rConf.db
        )

        self._rConf = _rConf
        self._stats = SeriesArray()

    def collect(self):
        # self._stats.extend([self._collectConnState])
        self._stats.append(self._collectConnState())
        
    def _collectConnState(self):
        _metric = "redis_connection_state"
        resp = self._cli.ping()
        state = 1 if resp else 0
        return Series(
            metric=_metric,
            value=state,
            tags={"host": self._rConf.host, "port": self._rConf.port}
        )

    def stats(self, format_: str="prometheus", realTime: bool=False) -> str:
        if realTime:
            self.collect()
        if format_ == "prometheus":
            return self._stats.prometheus()
        elif format_ == "json":
            return json.dumps(self._stats.opentsdb())
