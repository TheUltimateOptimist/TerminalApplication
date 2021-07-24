# this file contains all fuctions that have to do with training

# third party imports:

# first party imports:
import sql
import time
import color
import format
from GAUD import get,update,add


# functions:
# Get
def habits(showOperation, sqloperation):
    result = get.getIntern("habits", ["habits_name", "habits_count", "habits_done"], "habits_count < 100000 ORDER BY habits_done DESC", showOperation)
    color.printBlue("habits:")
    print("")
    i = 1
    for row in result:
        if str(row[2]) == "true":
            color.printGreen(str(i) + ". " + str(row[1]) + " " + str(row[0]))
        else:
            color.printRed(str(i) + ". " + str(row[1]) + " " + str(row[0])) 
        i = i + 1
    print("")
    color.printBlue("add habbit: 1 | habit done: 2")
    next = input("next: ")
    while next == "1" or next == "2":
        if next == "1":
            name = input("habits_name: ")
            description = input("description: ")
            add.addIntern("habits", ["all"], [name, description, "0", "false"], showOperation)
            next = input("next: ")
        elif next == "2":
            number = input("habit number: ")
            sql.execute(f"UPDATE habits SET habits_count = habits_count + 1, habits_done = 'true' WHERE habits_name = '{str(result[int(number) - 1][0])}'", showOperation)
            habits(showOperation, sqloperation) 


# Add

# Update
def habitdone(showOperation, sqloperation):
    count = get.getIntern("habits", ["habits_count"], "")
    update.updateIntern("habits", ["habits_date", "habits_count"], )

# Delete
