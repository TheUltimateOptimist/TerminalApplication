# contains all functions having to do with the tasks table

# third party imports:
from GAUD.update import updateIntern
import time
from colorama import init
from termcolor import colored

# first party imports:
import sql
import color
import format
import functions
from GAUD import get


# functions:
# Get:
def getTasks(showOperation, operation):
    init()  # initialize colors
    if operation.__contains__("-d"):
        return get.getIntern("tasks", ["priority", "title"], f"status = 1 AND completion = '{format.currentDate()}'", showOperation)
    else:
        resultOne = get.getIntern("tasks", [
                                  "priority", "title"], f"status = 0 AND (workondate = '{format.currentDate()}' OR workondate = '2020-12-12')", showOperation)
        resultTwo = get.getIntern("tasks", [
                                  "workondate"], f"status = 0 AND (workondate = '{format.currentDate()}' OR workondate = '2020-12-12')", showOperation)
        colors = []
        for i in range(len(resultTwo)):
            if str(resultTwo[i][0]) == "2020-12-12":
                colors.append("yellow")
            else:
                colors.append("red")
        if operation.__contains__("-c"):
            return colors
        else:
            return resultOne


# Add
def addTask(showOperation):
    title = input("title: ")
    if title != "":
        priority = int(input("priority: "))
        workondate = input("workondate: ")
        if workondate == "":
            workondate = "2020-12-12"
        if len(sql.execute(f"SELECT * FROM tasks WHERE title = '{title}'", showOperation)) == 0:
            sql.execute(
                f"INSERT INTO tasks Values('{title}', {priority}, 0, '{format.currentDate()}', NULL, 0, '{workondate}')", showOperation, "post")
        else:
            sql.execute(
                f"UPDATE tasks SET priority = {priority}, status = 0, initialization = '{format.currentDate()}', completion = NULL, workondate = '{workondate}' WHERE title = '{title}'", showOperation, "post")


# Update
def taskDone(showOperation, task):
    if task != "":
        count = sql.execute(
            f"SELECT count FROM tasks WHERE title = '{task}'", showOperation, "get")
        if len(count) > 0:
            date = time.localtime(time.time())
            sql.execute(
                f"UPDATE tasks SET status = 1, completion = '{date.tm_year}-{date.tm_mon}-{date.tm_mday}', count = {str(count[0][0])} WHERE title = '{task}'", showOperation, "post")
        else:
            color.printRed("ERROR: invalid name")


def tasks(showOperation, operation):
    result = getTasks(showOperation, "")
    functions.printTable(result, ["priority", "title"], "blue", getTasks(
        showOperation, "-c"), "blue", True)
    color.printBlue(
        "v: view done tasks | a: add new task | d: task done | w: change workondate")
    next = input("next: ")
    while next != "":
        if next == "v":
            functions.printTable(getTasks(
                showOperation, "-d"), ["priority", "title"], "blue", ["green"], "blue", showIndexes=True)
        elif next == "a":
            addTask(showOperation)
        elif next == "d":
            taskNumber = int(input("taskNumber: "))
            taskDone(showOperation, str(result[taskNumber - 1][1]))
        elif next == "w":
            taskNumber = int(input("taskNumber: "))
            newDate = input("new workondate: ")
            updateIntern("tasks", ["workondate"], [
                         newDate], f"title = '{str(result[taskNumber - 1][1])}'", showOperation)
        next = input("next: ")
