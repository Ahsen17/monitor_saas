import json
import os
from pathlib import Path
from common.meta import SingletonMeta
from common.serializer import JsonSerializable
from common.utils.parsers import TomlParser


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurations definition.
CONFIGS = TomlParser(os.path.join(BASE_DIR, 'configs/default.conf'))


class BaseConfig(JsonSerializable):
    def __init__(self):
        self._load()

    def _load(self, part: str=""):
        params = CONFIGS.get(part, {})
        for key, value in params.items():
            setattr(self, key, value)


class ServiceConfig(
    BaseConfig,
    metaclass=SingletonMeta
):
    def __init__(self):
        self._load(part="service")
    

class MysqlConfig(
    BaseConfig,
    metaclass=SingletonMeta
):
    def __init__(self):
        self._load(part="mysql")


class RedisConfig(
    BaseConfig,
    metaclass=SingletonMeta
):
    def __init__(self):
        self._load(part="redis")


class JwtConfig(
    BaseConfig,
    metaclass=SingletonMeta
):
    def __init__(self):
        self._load(part="jwt")


class EmailConfig(
    BaseConfig,
    metaclass=SingletonMeta
):
    def __init__(self):
        self._load(part="email")


class SystemConfig(
    BaseConfig,
    metaclass=SingletonMeta
):
    def __init__(self):
        self.serviceConf = ServiceConfig()
        self.mysqlConf = MysqlConfig()
        self.redisConf = RedisConfig()
        self.jwtConf = JwtConfig()
        self.emailConf = EmailConfig()

    def tojson(self):
        return json.dumps(CONFIGS.all())