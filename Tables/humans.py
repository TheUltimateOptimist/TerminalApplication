# contains all functions that have to do with the mitmenschen table

# third party imports:
from termcolor import colored
from colorama import init
# first party imports:
import sql
import color
from GAUD import get
import format


# mitmenschen spalten
spalten = ["Id: ", "Vorname: ", "Nachname: ", "Geburtsdatum: ", "Handynummer: ", "Beziehung: ", "Lieblingsessen: ","Mutter: ", "Vater: ", "Ehepartner: ", "Job: "]

# functions:
# Get:
def nget(showOperation, operation):
    columnName = operation.split(" ")[1]
    firstname = "'" + input("firstname: ") + "'"
    if firstname != "''":
        lastname = "'" + input("lastname: ") + "'"
        if columnName == "human":
            result = sql.execute(
                f"SELECT * FROM mitmenschen WHERE firstname = {firstname} AND lastname = {lastname}", showOperation)
            for i in range(len(result[0])):
                color.printBlue(
                    f"{get.getcolumnnames(showOperation, 'mitmenschen')[i][0]}: {format.toHumanDate(result[0][i])}")
        else:
            result = sql.execute(
                f"SELECT {columnName} FROM mitmenschen WHERE firstname = {firstname} AND lastname = {lastname}", showOperation)
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
            f"SELECT * FROM mitmenschen WHERE relation = {beziehung}", showOperation)
        if onlyNames:
            color.printBlue("Names: ")
            for f in result:
                color.printBlue(f[1] + " " + f[2])
        else:
            for i in result:
                s = ''
                for j in range(len(spalten)):
                    s = s + spalten[j] + \
                        colored(format.toHumanDate(i[j]), "blue") + ", "
                print(s)
        if operation.__contains__("-r") and beziehung != "":
            getgroup(showOperation, operation)


def nextbirthday(showOperation, operation):
    if operation.__contains__("-n"):
        number = int(input("number: "))
    else:
        number = 1
    result = sql.execute(
        f"SELECT birthday, firstname, lastname FROM mitmenschen WHERE DAYOFYEAR(birthday) >= DAYOFYEAR(CURDATE()) ORDER BY DAYOFYEAR(birthday);", showOperation)
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
    vorname = format.value(input("firstname: "))
    if vorname != "NULL":
        nachname = format.value(input("lastname: "))
        geburtsdatum = format.value(input("birthday: "))
        handynummer = format.value(input("phonenumber: "))
        beziehung = format.value(input("relation: "))
        lieblingsessen = format.value(input("favouritefood: "))
        mutter = format.value(input("mother: "))
        vater = format.value(input("father: "))
        ehepartner = format.value(input("spouse: "))
        job = format.value(input("job: "))
        sql.execute(
            f"INSERT INTO mitmenschen(firstname, lastname, birthday,  phonenumber, relation, favouritefood, mother, father, spouse, job) Values({vorname}, {nachname}, {geburtsdatum}, {handynummer}, {beziehung}, {lieblingsessen}, {mutter}, {vater}, {ehepartner},{job})", showOperation)
        color.printGreen("Human successfully added")
        if operation.__contains__("-r") and vorname != "":
            addhuman(showOperation, operation)

# Update:


# Delete:
