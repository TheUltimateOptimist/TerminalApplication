# contains all functions that have to do with formatting

# third party imports:
import math
import time

# first party imports:


# functions:
def formatZero(i):
    i = int(i)
    if i < 10 >= 0:
        return "0" + str(i)
    else:
        return str(i)


def toDate(seconds):
    t = time.localtime(seconds)
    return f"'{t.tm_year}-{t.tm_mon}-{t.tm_mday}'"


def fromDate(s):
    t = time.strptime(s, "%y-%m-%d")
    return t


def value(val):
    if val != "":
        if str(type(val)) == "<class 'int'>":
            return val
        else:
            return "'" + val + "'"
    else:
        return "NULL"


def toHumanDate(s):
    s = str(s)
    c = "2222-22-22"
    if len(s) == len(c):
        if s[4] == c[4] and s[7] == c[7]:
            w = s.split("-")
            return w[2] + "." + w[1] + "." + w[0]
        else:
            return s
    else:
        return s


def toClockTime(s):
    w = s.split(":")
    return formatZero(w[0]) + ":" + formatZero(w[1])


def secondsToHourMinuteFormat(seconds):
    h = math.floor(seconds / 3600)
    return f"{formatZero(h)}:{formatZero(round((seconds - h * 3600) / 60))}"
