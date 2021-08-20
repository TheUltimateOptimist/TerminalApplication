# this file contains all fuctions that have to do with training

# third party imports:

# first party imports:
import sql
import time
import color
import format
from GAUD import get


# functions:
def exerciseExists(exerciseName, showOperation):
    result = sql.execute(
        f"select exercises_id from exercises where exercises_name = '{exerciseName}'", showOperation, "get")
    if len(result) == 0:
        return False
    else:
        return True


def restTimer(seconds):
    while seconds > 0:
        time.sleep(1)
        seconds = seconds - 1
        color.printBlue(seconds)


def createTrainingPlan(showOperation, tid):
    name = input("name: ")
    if name != "":
        result = sql.execute(
            f"SELECT exercise_id, exercising_sets, exercising_rest FROM exercising WHERE exercising_training_id = {tid}", showOperation, "get")
        plan = []
        for row in result:
            plan.append([str(row[0]), str(row[1]), str(row[2])])
        sql.execute(
            f"INSERT INTO training_plan(training_plan_name, training_plan_description) VALUES('{name}', {createDescription(plan)})", showOperation, "post")
        tpid = str(sql.execute(
            f"select count(*) from training_plan", showOperation)[0][0], "get")
        for row in plan:
            sql.execute(
                f"INSERT INTO training_plan_parts(training_plan_parts_training_plan_id,training_plan_parts_exercise_id, training_plan_parts_sets, training_plan_parts_rest) VALUES({tpid}, {row[0]}, {row[1]}, {row[2]})", showOperation, "post")

# Get


def getExerciseId(exercise, showOperation):
    return int(sql.execute(f"SELECT exercises_id FROM exercises WHERE exercises_name = '{exercise}'", showOperation, "get")[0][0])


# Add
def addexercise(showOperation, operation):
    name = input("name: ")
    if name != "":
        sql.execute(
            f"INSERT INTO exercises(exercises_name) VALUES('{name}')", showOperation, "post")
        if operation.__contains__("-r"):
            addexercise(showOperation, operation)


def train(showOperation, operation):
    exercise = input("first exercise: ")
    if exercise != "":
        if exerciseExists(exercise, showOperation):
            currentTime = format.currentDateTime()
            print(currentTime)
            sql.execute(
                f"INSERT INTO training(training_date) VALUES('{currentTime}')", showOperation, "post")
            tid = str(sql.execute(
                f"SELECT training_id FROM training WHERE training_date = '{currentTime}'", showOperation)[0][0])
            while exercise != "":
                if exerciseExists(exercise, showOperation):
                    eid = str(sql.execute(
                        f"SELECT exercises_id FROM exercises WHERE exercises_name = '{exercise}'", showOperation, "get")[0][0])
                    rest = input("rest: ")
                    sets = input("sets: ")
                    reps = 0
                    for i in range(int(sets)):
                        reps = reps + int(input("reps: "))
                        if i < int(sets) - 1:
                            restTimer(int(rest))
                    sql.execute(
                        f"INSERT INTO exercising (exercise_id, exercising_training_id, exercising_sets, exercising_reps, exercising_rest) VALUES({eid}, {tid}, {sets}, {str(reps)}, {rest})", showOperation, "post")
                    exercise = input("next exercise: ")
                else:
                    color.printRed("ERROR: Exercise does not exist!")
                    exercise = input("next exercise: ")
        if exercise != "":
            color.printRed("ERROR: Exercise does not exist!")
        else:
            if input("create Training Plan? ") == "y":
                createTrainingPlan(showOperation, tid)


def getdevelopment(showOperation, operation):
    exercise = input("exercise: ")
    if exercise != "":
        resultOne = sql.execute(
            f"SELECT exercises_id from exercises WHERE exercises_name = '{exercise}'", showOperation, "get")
        print(resultOne)
        if len(resultOne) > 0:
            exercise_id = str(resultOne[0][0])
            resultTwo = sql.execute(
                f"SELECT exercising_reps from exercising WHERE exercise_id = {exercise_id}", showOperation, "post")
            print(resultTwo)
            s = "Entwicklung: "
            for element in resultTwo:
                s = s + str(element[0]) + ", "
            color.printBlue(s)
            if operation.__contains__("-r"):
                getdevelopment(showOperation, operation)
        else:
            color.printRed("ERROR: Exercise does not exist!")
            getdevelopment(showOperation, operation)


def createDescription(list):
    s = ""
    i = 1
    for l in list:
        if i < len(list):
            s = s + f"{l[1]}*{l[0]},"
            i = i + 1
        else:
            s = s + f"{l[1]}*{l[0]}"
    return s


def addtrainingplan(showOperation, operation):
    exercise = input("first exercise: ")
    if exercise != "":
        plan = []
        while exercise != "":
            sets = input("sets: ")
            rest = input("rest: ")
            plan.append([exercise, sets, rest])
            exercise = input("next exercise: ")
        name = input("name: ")
        description = createDescription(plan)
        sql.execute(
            f"INSERT INTO training_plan (training_plan_name, training_plan_description) VALUES('{name}', '{description}')",  showOperation, "post")
        tid = get.getIntern("training_plan", [
                            "training_plan_id"], f"training_plan_name = '{name}' AND training_plan_description = '{description}'", showOperation)[0][0]
        for row in plan:
            sql.execute(
                f"INSERT INTO training_plan_parts(training_plan_parts_exercise_id, training_plan_parts_training_plan_id, training_plan_parts_sets, training_plan_parts_rest) VALUES({getExerciseId(row[0], showOperation)}, {tid}, {row[1]}, {row[2]})", showOperation, "post")
        if operation.__contains__("-r"):
            addtrainingplan(showOperation, operation)


# Update

# Delete
    s = "s"
