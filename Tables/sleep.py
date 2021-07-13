# this file contains all functions that have to do with the table schlafrhythmus

# third party imports:
import time
import math
from termcolor import colored
from colorama import init

# first party imports:
import sql
import color
import format
from Tables import tasks


# functions:
# math:
def calculateSleepDuration(morning, evening):
    morning = time.mktime(time.strptime(morning, "%Y-%m-%d %H:%M:%S"))
    evening = time.mktime(time.strptime(evening, "%Y-%m-%d %H:%M:%S"))
    t = morning - evening
    if t < 0:
        t = 24 * 3600 - math.fabs(t)
        allSeconds = t
        h = math.floor(t / 3600)
        m = round((t - h * 3600) / 60)
    else:
        allSeconds = t
        h = math.floor(t / 3600)
        m = round(t - h * 3600)
    return [h, m, allSeconds]


def average(intList):
    v = 0
    for i in intList:
        v = v + i
    return round(v / len(intList))


def calculateAverageBedTime(result, id):
    # id = 1: morning
    # id = 2: evening
    minutes = 0
    for r in result:
        minutes = minutes + \
            int(str(r[id]).split(":")[0])*60 + int(str(r[id]).split(":")[1])
    return format.secondsToHourMinuteFormat(round(minutes/len(result))*60)


# Get:
def sevendays(showOperation, operation):
    result = sql.execute(
        f"SELECT * FROM schlafrhythmus WHERE datum <= {format.toDate(time.time())} AND datum >= {format.toDate(time.time() - 7 * 86400)}", showOperation)
    sleepDurations = []
    for i in range(len(result) - 1):
        sleepDurations.append(
            calculateSleepDuration('2021-12-12' + " " + str(result[i + 1][1]),
                                   '2021-12-12' + " " + str(result[i][2]))[2])
    for row in result:
        color.printBlue(
            format.toHumanDate(row[0]) + " " + "Morgens: " + format.toClockTime(str(row[1])) + ", " + "Abends: " + format.toClockTime(
                str(row[2])))
    color.printMagenta(
        f"Du hast durchschnittlich {format.secondsToHourMinuteFormat(average(sleepDurations))} Stunden geschlafen")
    color.printMagenta(
        f"Du bist durchschnittlich um {calculateAverageBedTime(result, 1)} aufgestanden")
    color.printMagenta(
        f"Du bist durchschnittlich um {calculateAverageBedTime(result, 2)} schlafen gegangen")


# Add
def tobed(showOperation, operation):
    init()  # initialize colors
    if time.localtime(time.time()).tm_hour < 10:
        currentTime = time.localtime(time.time() - 86400)
    else:
        currentTime = time.localtime(time.time())
    done = sql.execute(
        "SELECT title, priority FROM tasks WHERE status = 1 ORDER BY priority DESC", showOperation)
    opentasks = sql.execute(
        "SELECT title, priority FROM tasks WHERE status = 0 ORDER BY priority DESC", showOperation)
    for row in done:
        color.printGreen(f"{str(row[0])}")
        s = input(f"")
    for row in opentasks:
        print(f"{str(row[1])} | {colored(str(row[0]), 'red')}")
        s = input(f"")
    sql.execute(
        f"UPDATE schlafrhythmus SET abends = '{currentTime.tm_hour}:{currentTime.tm_min}:{currentTime.tm_sec}' WHERE datum = '{currentTime.tm_year}-{currentTime.tm_mon}-{currentTime.tm_mday}'", showOperation)
    color.printGreen("Good Night")


def frombed(showOperation, operation):
    currentTime = time.localtime(time.time())
    sql.execute(
        f"INSERT INTO schlafrhythmus VALUES('{currentTime.tm_year}-{currentTime.tm_mon}-{currentTime.tm_mday}', '{currentTime.tm_hour}:{currentTime.tm_min}:{currentTime.tm_sec}', '00:00:00')", showOperation)
    color.printGreen("time added")
    tasks.gettasks(False, "")
