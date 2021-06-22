import math


def tab_to_space(text, tab_size=4):
    TAB = "\t"
    SPACE = " "
    lines = text.split("\n")
    results = []
    for line in lines:
        cache = str()
        for char in line:
            if char == TAB:
                while len(cache) % tab_size != 0:
                    cache += SPACE
            else:
                cache += char
        results.append(cache)
    return "\n".join(results)


def convert_size(size):
    """ Size should be in bytes.
    Return a tuple (float_or_int_val, str_unit) """
    if size == 0:
        return (0, "B")
    KILOBYTE = 1024
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, KILOBYTE)))
    p = math.pow(KILOBYTE, i)
    result = round(size/p, 2)
    return (result, size_name[i])


def truncate_str(data, max_size=15, ellipsis="..."):
    val = ((data[:max_size] + ellipsis)
            if len(data) > max_size else data)
    return val