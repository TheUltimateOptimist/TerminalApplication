# this file contains the fuctions that have to do with projects

# third party imports:

# first party imports:
from GAUD import get, update, delete, add
import color
import sql


# not included in terminal language
def steps(id, showOperation):
    result = get.getIntern("steps", ["steps_name", "steps_number", "steps_status"], f"steps_project_id = {str(id)}", showOperation)
    for row in result:
        if int(row[2]) == 0:
            color.printBlue(f"{row[1]}. {row[0]}")
        else:
            color.printGreen(f"{row[1]}. {row[0]}")    
    print("1: add step | 2: step done | 3: delete step")
    next = input("next: ")
    while next != "":
        if next == "1":
            title = input("title: ")
            number = input("number: ")
            if number == "":
                number = len(result) + 1
            else:
                sql.execute(f"UPDATE steps SET steps_number = steps_number + 1 WHERE steps_number >= {number}",showOperation) 
            add.addIntern("steps", ["all except id"], [title, int(number), 0, id], showOperation)
        elif next == "2":
            number = input("number: ")
            update.updateIntern("steps", ["steps_status"], [1], f"steps_name = '{result[int(number) - 1][0]}'", showOperation)
        elif next == "3":
            number = input("number: ")
            sql.execute(f"UPDATE steps SET steps_number = steps_number + -1 WHERE steps_number > {number}" ,showOperation)
            sql.execute(f"DELETE FROM steps WHERE steps_name = '{result[int(number) - 1][0]}'" ,showOperation) 
        steps(id, showOperation)       


# included in terminal language
def projects(showOperation, operation):
    result = get.getIntern("projects", ["projects_name", "projects_id"], "", showOperation)
    i = 1
    for row in result:
        color.printBlue(f"{str(i)}. {row[0]}")
        i = i + 1
    print("")
    print(f"a: add project | r: remove project | specific number: select project")
    next = input("next: ")
    if next != "":
        if next == "a":
            title = input("title: ")
            description = input("description: ")
            add.addIntern("projects", ["all except id"], [title, description], showOperation)
        elif next == "r":
            number = input("number: ")
            sql.execute(f"DELETE FROM projects WHERE projects_name = '{result[int(number) -1][0]}'",showOperation)
        else:
            steps(result[int(next) - 1][1], showOperation) 
        projects(showOperation, operation)         
