# contains all functions that have to do with the mitmenschen table

# third party imports:
from GAUD.add import addIntern
from termcolor import colored
from colorama import init
# first party imports:
import sql
import color
from GAUD import get
import format
import functions


# mitmenschen spalten
spalten = ["Id: ", "Vorname: ", "Nachname: ", "Geburtsdatum: ", "Handynummer: ",
           "Beziehung: ", "Lieblingsessen: ", "Mutter: ", "Vater: ", "Ehepartner: ", "Job: "]

# functions:
# Get:


def nget(showOperation, operation):
    columnName = operation.split(" ")[1]
    firstname = "'" + input("firstname: ") + "'"
    if firstname != "''":
        lastname = "'" + input("lastname: ") + "'"
        if columnName == "human":
            result = sql.execute(
                f"SELECT * FROM mitmenschen WHERE firstname = {firstname} AND lastname = {lastname}", showOperation, "get")
            for i in range(len(result[0])):
                color.printBlue(
                    f"{get.getcolumnnames(showOperation, 'mitmenschen')[i][0]}: {format.toHumanDate(result[0][i])}")
        else:
            result = sql.execute(
                f"SELECT {columnName} FROM mitmenschen WHERE firstname = {firstname} AND lastname = {lastname}", showOperation, "get")
            color.printBlue(
                f"{columnName}: {format.toHumanDate(result[0][0])}")
        if operation.__contains__("-r") and columnName != "":
            nget(showOperation, operation)


def getgroup(showOperation, operation):
    init()  # initialize colors
    if operation.__contains__("-n"):
        onlyNames = True
    else:
        onlyNames = False
    beziehung = "'" + input("Beziehung: ") + "'"
    if beziehung != "":
        result = sql.execute(
            f"SELECT * FROM mitmenschen WHERE relation = {beziehung}", showOperation, "get")
        if onlyNames:
            color.printBlue("Names: ")
            for f in result:
                color.printBlue(f[1] + " " + f[2])
        else:
            functions.printTable(result, functions.toOneDimList(get.getcolumnnames(
                showOperation, "mitmenschen"), 0), "blue", ["blue"], "blue", showIndexes=True)
        if operation.__contains__("-r") and beziehung != "":
            getgroup(showOperation, operation)


def nextbirthday(showOperation, operation):
    if operation.__contains__("-n"):
        number = int(input("number: "))
    else:
        number = 1
    result = sql.execute(
        f"SELECT birthday, firstname, lastname FROM mitmenschen WHERE DAYOFYEAR(birthday) >= DAYOFYEAR(CURDATE()) ORDER BY DAYOFYEAR(birthday);", showOperation, "get")
    if len(result) > 0:
        for i in range(number):
            date = str(result[i][0]).split("-")[2] + "." + \
                str(result[i][0]).split("-")[1]
            color.printBlue(
                date + " " + str(result[i][1]) + " " + str(result[i][2]))
    else:
        color.printBlue("Nobody")


# Add:
def addhuman(showOperation, operation):
    values = []
    values.append(input("firstname: "))
    if values[0] != "":
        values.append(input("lastname: "))
        values.append(input("birthday: "))
        values.append(input("phonenumber: "))
        values.append(input("relation: "))
        values.append(input("favouritefood: "))
        values.append(input("mother: "))
        values.append(input("father: "))
        values.append(input("spouse: "))
        values.append(input("job: "))
        addIntern("mitmenschen", ["all except id"], values, showOperation)
        color.printGreen("Human successfully added")
        if operation.__contains__("-r") and values[0] != "":
            addhuman(showOperation, operation)

# Update:


# Delete:
