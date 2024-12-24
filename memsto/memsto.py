import copy
import threading
import time


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

    def _outOfArrBound(self, index: int) -> bool:
        # index out of edge
        return (index < -self._arrLen or index >= self._arrLen)

    def addArrEle(self, ele: any) -> bool:
        if ele:
            self._arr.append(ele)
            self._arrLen += 1
            return True
        return False
    
    def delArrEle(self, index: int) -> bool:
        if self._outOfArrBound(index):
            return False

        _array = self._arr
        index = index if index>=0 else abs(index) + 1
        _array = _array[0:index] + _array[index+1:]
        self._arrLen -= 1

        return True
    
    def getArrEle(self, index: int) -> any:
        if self._outOfArrBound(index):
            return None
        return copy.deepcopy(self._arr[index])
    
    def getArrLen(self) -> int:
        return self._arrLen
    
    def addEntry(self, key: str, val: any) -> bool:
        if not key or key in self._dict:
            return False
        self._dict[key] = val
        return True
    
    def delEntry(self, key: str) -> any:
        if key in self._dict:
            tmp = copy.deepcopy(self._dict[key])
            del self._dict[key]
            return tmp
        return None
    
    def getVal(self, key: str) -> any:
        if key in self._dict:
            return copy.deepcopy(self._dict[key])
        return None
        

class UnsafeCache(object):
    def __init__(self):
        self._cache = _memSto()

    def addEle(self, ele: any) -> bool:
        return self._cache.addArrEle(ele)
    
    def delEle(self, index: int) -> any:
        ele = self._cache.getArrEle(index)
        self._cache.delArrEle(index)
        return ele
   
    def pushEle(self, ele: any) -> bool:
        self.addEle(ele)
    
    def popEle(self) -> any:
        return self.delEle(-1)
    
    def getEle(self, index: int) -> any:
        return self._cache.getArrEle(index)
    
    def getLen(self) -> int:
        return self._cache.getArrLen()

    def addEntry(self, key: str, val: any) -> bool:
        return self._cache.addEntry(key, val)

    def delEntry(self, key: str) -> any:
        return self._cache.delEntry(key)

    def getVal(self, key: str) -> any:
        return self._cache.getVal(key)


class ConcurrencySafetyCache(UnsafeCache, Lockable):
    def __init__(self):
        self._lock = threading.Lock()
        super().__init__()


class SegmentMemStorage(object):
    def __init__(self, capacity: int = 5):
        self._capacity = capacity
        self._caches = [ConcurrencySafetyCache() for _ in range(capacity)]

    def _index(self, key: str = None, index: int = None) -> int:
        mod = self._capacity
        if key != None:
            return int(str(key.__hash__())[-5:]) % mod
        if index != None:
            index = index if index >=0 else abs(index) - 1
            return index % mod
        return mod + 1
    
