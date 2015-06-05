import json


def dump(obj, fp, *args, **kwargs):
    return json.dump(compress(obj), fp, *args, **kwargs)


def dumps(obj, *args, **kwargs):
    return json.dumps(compress(obj), *args, **kwargs)


def load(fp, *args, **kwargs):
    return uncompress(json.load(fp, *args, **kwargs))


def loads(s, *args, **kwargs):
    return uncompress(json.loads(s, *args, **kwargs))


def pack(dict_list):
    length = len(dict_list)
    keys = length and dict_list[0].keys() or []
    klength = len(keys)
    result = []
    i = 0
    while i < length:
        o = dict_list[i]
        ki = 0
        while ki < klength:
            result.append(o[keys[ki]])
            ki = ki + 1
        i = i + 1
    return [klength] + keys + result


def unpack(hlist):
    length = len(hlist)
    klength = hlist[0]
    result = []
    i = 1 + klength
    while i < length:
        o = dict()
        ki = 0
        while ki < klength:
            ki = ki + 1
            o[hlist[ki]] = hlist[i]
            i = i + 1
        result.append(o)
    return result


def compress(data):
    if isinstance(data, list):
        for idx, item in enumerate(data):
            item = compress(item)
            data[idx] = item

        try:
            return pack(data)
        except Exception as err:
            # Not packable data
            return data
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = compress(value)
        return data
    else:
        return data


def uncompress(data):
    if isinstance(data, list):
        for idx, item in enumerate(data):
            item = uncompress(item)
            data[idx] = item

        try:
            return unpack(data)
        except Exception as err:
            # Not packable data
            return data
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = uncompress(value)
        return data
    else:
        return data
