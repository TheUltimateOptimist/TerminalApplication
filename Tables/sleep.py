# this file contains all functions that have to do with the table schlafrhythmus

# third party imports:
from GAUD.get import getIntern
from GAUD.add import addIntern
import time
from termcolor import colored
from colorama import init

# first party imports:
import sql
import color
import format
from Tables import tasks


# functions:
# math:
def average(intList):
    v = 0
    for i in intList:
        v = v + i
    return round(v / len(intList))

# Get:
def sevendays(showOperation, operation):
    result = sql.execute(
        f"SELECT * FROM sleep WHERE date <= {format.toDate(time.time())} AND date >= {format.toDate(time.time() - 7 * 86400)}", showOperation)
    if len(result) > 0:    
        sleepDurations = []
        morningTimes = []
        eveningTimes = []
        for row in result:
            et = time.strptime(str(row[1]), "%Y-%m-%d %H:%M:%S")
            mt = time.strptime(str(row[2]), "%Y-%m-%d %H:%M:%S")
            d = time.strptime(str(row[0]) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            morningTimes.append(time.mktime(mt) - time.mktime(d))
            eveningTimes.append(time.mktime(et) - time.mktime(d))
            sleepDurations.append(time.mktime(mt) - time.mktime(et))
        for row in result:
            color.printBlue(format.toHumanDate(str(row[0])) + " " + "Abends: " + str(row[1]).split(" ")[1] + ", " + "Morgens: " + str(row[2]).split(" ")[1])
        color.printMagenta(
            f"Du hast durchschnittlich {format.secondsToHourMinuteFormat(average(sleepDurations))} Stunden geschlafen")
        color.printMagenta(
            f"Du bist durchschnittlich um {format.secondsToHourMinuteFormat(average(morningTimes) % 86400)} aufgestanden")
        color.printMagenta(
            f"Du bist durchschnittlich um {format.secondsToHourMinuteFormat(average(eveningTimes) % 86400)} schlafen gegangen")


# Add
def tobed(showOperation, operation):
    init()  # initialize colors
    if time.localtime(time.time()).tm_hour < 10:
        currentTime = time.localtime(time.time() - 86400)
    else:
        currentTime = time.localtime(time.time())
    done = sql.execute(
        f"SELECT title, priority FROM tasks WHERE status = 1 AND completion = '{currentTime.tm_year}-{currentTime.tm_mon}-{currentTime.tm_mday}' ORDER BY priority DESC", showOperation)
    opentasks = sql.execute(
        f"SELECT title, priority FROM tasks WHERE status = 0 AND (workondate = '2020-12-12' OR workondate = '{currentTime.tm_year}-{currentTime.tm_mon}-{currentTime.tm_mday}') ORDER BY priority DESC", showOperation)
    for row in done:
        color.printGreen(f"{str(row[0])}")
        s = input(f"")
    for row in opentasks:
        print(f"{str(row[1])} | {colored(str(row[0]), 'red')}")
        s = input(f"")
    print("")
    result = getIntern("habits", ["habits_name", "habits_count", "habits_done"], "habits_count < 100000 ORDER BY habits_done DESC", showOperation)
    color.printBlue("habits:")
    print("")
    i = 1
    for row in result:
        if str(row[2]) == "true":
            color.printGreen(str(i) + ". " + str(row[1]) + " " + str(row[0]))
        else:
            color.printRed(str(i) + ". " + str(row[1]) + " " + str(row[0])) 
            sql.execute(f"UPDATE habits SET habits_count = 0 WHERE habits_name = '{row[0]}'", showOperation)
        i = i + 1  
    sql.execute(f"UPDATE habits SET habits_done = 'false'", showOperation)      
    sql.execute(
        f"INSERT INTO sleep(date, evening) VALUES('{currentTime.tm_year}-{currentTime.tm_mon}-{currentTime.tm_mday}', '{format.currentDateTime()}')", showOperation)
    color.printGreen("Good Night")


def frombed(showOperation, operation):
    sql.execute(f"UPDATE sleep SET morning = '{format.currentDateTime()}' WHERE morning IS NULL", showOperation)
    color.printGreen("time added")
    tasks.printTasks(tasks.getTasks(False, ""), "red")
    print("")
    result = getIntern("habits", ["habits_name", "habits_count", "habits_done"], "habits_count < 100000 ORDER BY habits_done DESC", showOperation)
    color.printBlue("habits:")
    print("")
    i = 1
    for row in result:
        if str(row[2]) == "true":
            color.printGreen(str(i) + ". " + str(row[1]) + " " + str(row[0]))
        else:
            color.printRed(str(i) + ". " + str(row[1]) + " " + str(row[0])) 
        i = i + 1

