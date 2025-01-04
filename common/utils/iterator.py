class ListIterator(object):
    def __init__(self):
        self._arr = []
        self._arrLen = 0
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= self._arrLen:
            raise StopIteration
        _res = self._arr[self._index]
        self._index += 1
        return _res
