import json
from typing import Dict


class JsonSerializable:
    """
    refactor __dict__ while implement
    """

    def toJson(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, jsonStr: str) -> Dict:
        if not jsonStr:
            return {}
        
        try:
            jsonObj = json.loads(jsonStr)
        except json.JSONDecodeError:
            return {}
        return cls(**jsonObj)