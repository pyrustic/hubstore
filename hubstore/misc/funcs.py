import math


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


def badass_iso_8601_date_parser(date):
    # YYYY-MM-DDTHH:MM:SSZ
    date = date.rstrip("Z")
    date_part, time_part = date.split("T")
    months = ("January", "February", "March", "April", "May",
              "June", "July", "August", "September", "October",
              "November", "December")
    year, month, day = date_part.split("-")
    text = "{month} {day}, {year} at {time} UTC".format(month=months[int(month) - 1],
                                          day=day, year=year, time=time_part)
    return text


def dirty_metadata_parser(path):
    data = []
    with open(path, "r") as file:
        for line in file.readlines():
            key = ""
            value = ""
            parsing_key = True
            parsing_value = False
            cache = ""
            if line == "\n":
                break
            for char in line:
                if parsing_key and char == ":":
                    parsing_key = False
                    key = cache
                    cache = ""
                    continue
                if not parsing_key and not parsing_value:
                    parsing_value = True
                    continue
                if parsing_value and char == "\n":
                    value = cache
                    data.append((key, value))
                cache += char
    return data