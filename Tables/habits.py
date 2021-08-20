# this file contains all fuctions that have to do with training

# third party imports:

# first party imports:
import sql
import time
import color
import format
from GAUD import get, update, add
import functions


# functions:
# Get
def habits(showOperation, sqloperation):
    result = get.getIntern("habits", ["habits_name", "habits_count", "habits_done"],
                           "habits_count < 100000 ORDER BY habits_done DESC", showOperation)
    color.printBlue("habits:")
    print("")
    entryColors = []
    for row in result:
        if row[2] == "true":
            entryColors.append("green")
        else:
            entryColors.append("red")
    functions.printTable(result, ["name", "count", "done?"],
                         "blue", entryColors, "blue", showIndexes=True)
    print("")
    color.printBlue("add habbit: a | habit done: d")
    next = input("next: ")
    while next == "a" or next == "d":
        if next == "a":
            name = input("habits_name: ")
            description = input("description: ")
            add.addIntern("habits", ["all"], [
                          name, description, "0", "false"], showOperation)
            next = input("next: ")
        elif next == "d":
            number = input("habit number: ")
            sql.execute(
                f"UPDATE habits SET habits_count = habits_count + 1, habits_done = 'true' WHERE habits_name = '{str(result[int(number) - 1][0])}'", showOperation, "post")
            habits(showOperation, sqloperation)


# Add

# Update

# Delete
