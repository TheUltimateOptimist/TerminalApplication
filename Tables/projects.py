# this file contains the fuctions that have to do with projects

# third party imports:

# first party imports:
from GAUD import get, update, delete, add
import color
import sql
import functions

# not included in terminal language


def steps(id, showOperation):
    result = get.getIntern("steps", ["steps_number", "steps_name",
                           "steps_status"], f"steps_project_id = {str(id)}", showOperation)
    entryColors = []
    for row in result:
        if int(row[2]) == 0:
            entryColors.append("red")
        else:
            entryColors.append("green")
    functions.printTable(
        result, ["number", "name", "status"], "blue", entryColors, "blue")
    print("a: add step | d: step done | r: remove step")
    next = input("next: ")
    if next != "":
        if next == "a":
            title = input("title: ")
            number = input("number: ")
            if number == "":
                number = len(result) + 1
            else:
                sql.execute(
                    f"UPDATE steps SET steps_number = steps_number + 1 WHERE steps_number >= {number}", showOperation, "post")
            add.addIntern("steps", ["all except id"], [
                          title, int(number), 0, id], showOperation)
        elif next == "d":
            number = input("number: ")
            update.updateIntern("steps", ["steps_status"], [
                                1], f"steps_name = '{result[int(number) - 1][1]}'", showOperation)
        elif next == "r":
            number = input("number: ")
            sql.execute(
                f"UPDATE steps SET steps_number = steps_number + -1 WHERE steps_number > {number}", showOperation, "post")
            sql.execute(
                f"DELETE FROM steps WHERE steps_name = '{result[int(number) - 1][1]}'", showOperation, "post")
        steps(id, showOperation)


# included in terminal language
def projects(showOperation, operation):
    result = get.getIntern(
        "projects", ["projects_name", "projects_id"], "", showOperation)
    functions.printTable(result, ["name", "id"], "blue", [
                         "blue"], "blue", showIndexes=True)
    print("")
    print(f"a: add project | r: remove project | specific number: select project")
    next = input("next: ")
    if next != "":
        if next == "a":
            title = input("title: ")
            description = input("description: ")
            add.addIntern("projects", ["all except id"], [
                          title, description], showOperation)
        elif next == "r":
            number = input("number: ")
            sql.execute(
                f"DELETE FROM projects WHERE projects_name = '{result[int(number) -1][0]}'", showOperation, "post")
        else:
            steps(result[int(next) - 1][1], showOperation)
        projects(showOperation, operation)
