# contains all functions having to do with the tasks table

# third party imports:
import time
from colorama import init
from termcolor import colored

# first party imports:
import sql
import color

# functions:
# Get:
def gettasks(showOperation, operation):
    init()  # initialize colors
    if operation.__contains__("-d"):
        status = 1
        color = "green"
        t = time.localtime(time.time())
        addition = f" AND completion = '{t.tm_year}-{t.tm_mon}-{t.tm_mday}'"
    else:
        status = 0
        color = "red"
        addition = ""
    result = sql.execute(
        f"SELECT title, priority FROM tasks WHERE status = {status}{addition} ORDER BY priority DESC", showOperation)
    if len(result) == 0:
        color.printGreen("No Tasks")
    else:
        for row in result:
            print(f"{str(row[1])} | {colored(str(row[0]), color)}")
            s = input("")

# Add
def addtask(showOperation, operation):
    if operation.__contains__("-h"):
        print("lets you add a task to the list of tasks")
    else:
        title = input("title: ")
        if title != "":
            priority = input("priority: ")
            date = time.localtime(time.time())
            if len(sql.execute(f"SELECT * FROM tasks WHERE title = '{title}'", showOperation)) == 0:
                sql.execute(
                    f"INSERT INTO tasks Values('{title}', {priority}, 0, '{date.tm_year}-{date.tm_mon}-{date.tm_mday}', NULL)", showOperation)
            else:
                sql.execute(
                    f"UPDATE tasks SET priority = {priority}, status = 0, initialization = '{date}', completion = NULL WHERE title = '{title}' ", showOperation)
            if operation.__contains__("-r") and title != "":
                addtask(showOperation, operation)


# Update
def taskdone(showOperation, operation):
    task = input("task: ")
    if task != "":
        if len(sql.execute(f"SELECT * FROM tasks WHERE title = '{task}'"), showOperation) > 0:
            date = time.localtime(time.time())
            sql.execute(
                f"UPDATE tasks SET status = 1, completion = '{date.tm_year}-{date.tm_mon}-{date.tm_mday}' WHERE title = '{task}'", showOperation)
            if operation.__contains__("-r") and task != "":
                taskdone(showOperation, operation)
        else:
            color.printRed("ERROR: invalid name")
            taskdone(showOperation, operation)
