from typing import Any, Dict
from common.exceptions import ConfigParseError


class TomlParser(object):
    def __init__(self, filename: str = ""):
        import toml
        try:
            self._settings = toml.load(filename)
        except FileNotFoundError as e:
            raise e
        except:
            raise ConfigParseError(f"Failed to parse TOML file: {filename}")
    
    def get(self, part: str, key: str="", default=None) -> Any:
        if part not in self._settings:
            return default
        if not key:
            return self._settings[part]
        if key not in self._settings[part]:
            return default
        return self._settings[part][key]
    
    def all(self) -> Dict:
        return self._settings