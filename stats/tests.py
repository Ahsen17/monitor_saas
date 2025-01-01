from django.test import TestCase

# Create your tests here.

data = 'cpu_usage{ident="0",tags="a,b,c"} 0.1'
data = 'cpu_usage{ident="0",tags="a"} 0.1'
data = 'cpu_usage 0.1'
data = 'cpu_usage{} 0.1'

def testTransProm2Dict():
    # if '{' in data, then metric is the str before '{'
    # if not, then metric is the str before ' '
    if '{' in data:
        metric = data.split('{')[0]
    else:
        metric = data.split(' ')[0]
    
    # if '{' and '}' are in data, then tags are between '{' and '}'
    # if not, then there is no tags
    if '{' in data and '}' in data:
        tags = data.split('{')[1].split('}')[0]
    else:
        tags = ''

    # val is behind the ' '
    val = float(data.split(' ')[1])

    # tags analysis:
    # if tags are empty, then return a dict with metric and val
    if not tags:
        return {"metric": metric, "tags": {}, "value": val}
    # if not, there may be such situation:
    # 1. no comma in tagVal, as 'a="1",b="2"'
    # 2. comma in tagVal, as 'a="1,2,3",b="4,5,6"'
    # check situation above and split tagKey and tagVal in tags
    # analyze tags str foreach by char
    _p, _flag = 0, False
    _keyLst, _valLst = [], []
    for idx, c in enumerate(tags):
        if idx < _p: continue
        if _p >= len(tags): break
        if c == '=':
            _keyLst.append(tags[_p:idx])
            _p = idx + 1
            continue
        if c == '"':
            if not _flag:
                _p = idx + 1
                _flag = True
                continue
            else:
                _valLst.append(tags[_p:idx])
                _p = idx + 2
                _flag = False
                continue
    
    tags = {k: v for k,v in zip(_keyLst, _valLst)}

    # return a dict with metric, tags and val
    return {"metric":metric, "tags": tags, "value": val}


print(testTransProm2Dict())