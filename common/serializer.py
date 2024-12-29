import json
from typing import Dict


class JsonSerializable:
    def toJson(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, jsonStr: str) -> Dict:
        if not jsonStr:
            return {}
        
        try:
            jsonDic = json.loads(jsonStr)
        except json.JSONDecodeError:
            return {}
        return cls(**jsonDic)