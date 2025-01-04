"""
Not test yet.
"""


import traceback
from common.logger import debugLogger as log
from memsto.memsto import MultiSegmentSafetyCache, UnsafetyCache


def TestUnsafetyCache():
    try:
        cache = UnsafetyCache()
        cache.addEle(1)
        log.debug(cache.getEle(0))
        log.debug(cache.getLen())
        cache.delEle(0)
        log.debug(cache.getLen())

        cache.addEntry("k", "v")
        log.debug(cache.getVal("k"))
        log.debug(cache.getSize())
        cache.delEntry("k")
        log.debug(cache.getSize())
    except Exception as e:
        log.error(f"TestUnsafetyCache failed: {e}, \n {traceback.format_exc()}")


def TestCacheIterator():
    cache = UnsafetyCache()
    cache.addEle(1)
    cache.addEle(2)
    for ele in cache:
        log.debug(ele)


def TestSafetyCache():
    pass


def TestMultiSegmentSafetyCache():
    try:
        cache = MultiSegmentSafetyCache()
        cache.addEle(1)
        log.debug(cache.getEle(0))
        log.debug(cache.getLen())
        cache.delEle(0)
        log.debug(cache.getLen())

        cache.addEntry("k", "v")
        log.debug(cache.getVal("k"))
        log.debug(cache.getSize())
        cache.delEntry("k")
        log.debug(cache.getSize())
    except Exception as e:
        log.error(f"TestMultiSegmentSafetyCache failed: {e}, \n {traceback.format_exc()}")