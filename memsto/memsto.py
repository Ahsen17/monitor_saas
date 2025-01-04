"""
usage: cache list or dict

list func: addEle, pushEle, getEle, popEle, delEle, getLen
dict func: addEntry, delEntry, getVal, getSize

"""

import copy
import threading
from typing import Any

from common.exceptions import OutOfBounds, LeakageOfArgument


class Lockable(object):
    """
    desc: instance method full lock when w/r
    """
    def __init__(self):
        self._lock = threading.Lock()

    def __getattribute__(self, name: str):
        def _lockAndCall(lock, func, *args, **kwargs):
            with lock:
                return func(*args, **kwargs)
            
        attr = object.__getattribute__(self, name)

        if callable(attr) and not name.startswith('__'):
            return lambda *args, **kwargs: _lockAndCall(self._lock, attr, *args, **kwargs)
        
        return attr


class _memSto(object):
    def __init__(self):
        self._arr = []
        self._arrLen = 0
        self._dict = {}
        self._dicSize = 0

    def addEle(self, ele: Any) -> bool:
        if ele:
            self._arr.append(ele)
            self._arrLen += 1
            return True
        return False
    
    def delEle(self, index: int) -> Any:
        assert index >= -self._arrLen and index < self._arrLen, OutOfBounds()

        _array = self._arr
        index = index if index>=0 else index + self._arrLen
        res, _array = _array[index], _array[0:index] + _array[index+1:]
        self._arrLen -= 1

        return res
    
    def getEle(self, index: int) -> Any:
        assert index >= -self._arrLen and index < self._arrLen, OutOfBounds()
        return copy.deepcopy(self._arr[index])
    
    def getLen(self) -> int:
        """return list length"""
        return self._arrLen
    
    def addEntry(self, key: str, val: Any) -> bool:
        """
        if key exists, update val
        """
        if not key:
            return False
        if key not in self._dict:
            self._dicSize += 1
        self._dict[key] = val
        return True
    
    def delEntry(self, key: str) -> Any:
        if key in self._dict:
            tmp = copy.deepcopy(self._dict[key])
            del self._dict[key]
            self._dicSize -= 1
            return tmp
        return None
    
    def getVal(self, key: str) -> Any:
        if key in self._dict:
            return copy.deepcopy(self._dict[key])
        return None
    
    def getKeys(self) -> list:
        return copy.deepcopy(list(self._dict.keys()))
    
    def getVals(self) -> list:
        return copy.deepcopy(list(self._dict.values()))
    
    def getSize(self) -> int:
        """return entries size"""
        return self._dicSize
        

class UnsafetyCache(_memSto):
    def __init__(self):
        super().__init__()


class SafetyCache(UnsafetyCache, Lockable):
    def __init__(self):
        self._lock = threading.Lock()
        super().__init__()


class MultiSegmentSafetyCache(object):
    def __init__(self, capacity: int=5):
        self._capacity = capacity  # default 5 buckets
        self._caches = [SafetyCache() for _ in range(capacity)]

    def _segment(self, key: str = None, index: int = None) -> SafetyCache:
        _des = mod = self._capacity

        # calc segment index
        if key != None:
            _des = int(str(key.__hash__())[-5:]) % mod
        if index != None:
            index = index if index >=0 else index + self._arrLen
            _des = index % mod

        if _des >= self._capacity:
            raise OutOfBounds()
        return self._caches[_des]
    
    def addEle(self, ele: Any) -> bool:
        segment = self._segment(index=self._arrLen)
        if segment.addEle(ele):
            return True
        return False
    
    def delEle(self, index: int) -> Any:
        assert index >= -self._arrLen and index < self._arrLen, OutOfBounds()

        segment = self._segment(index=index)
        return segment.delEle(index // self._capacity)
    
    def getEle(self, index: int) -> Any:
        assert index >= -self._arrLen and index < self._arrLen, OutOfBounds()

        segment = self._segment(index=index)
        return segment.getEle(index // self._capacity)
    
    def getLen(self) -> int:
        """return list length"""
        return sum([segment.getLen() for segment in self._caches])
    
    def addEntry(self, key: str, val: Any) -> bool:
        segment = self._segment(key=key)
        if segment.addEntry(key, val):
            return True
        return False
    
    def delEntry(self, key: str) -> Any:
        segment = self._segment(key=key)
        return segment.delEntry(key)
    
    def getVal(self, key: str) -> Any:
        segment = self._segment(key=key)
        return segment.getVal(key)
    
    def getSize(self) -> int:
        """return entries size"""
        return sum([segment.getSize() for segment in self._caches])