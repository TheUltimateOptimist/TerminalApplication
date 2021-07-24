# file contains functions needed for executing sql operations

# third party imports:
from mysql.connector import connect, Error

# first party imports:
import color
import format
import functions

# functions:


def execute(sqloperation, showOperation):
    """
    param1: String sqloperation -> sql operation to execute
    param2: Boolean showOperation -> should it print the sql operation
    connects to personal_database and executes the given sql operation returning the query result
    prints the sql operation if showOperation = True
    """
    try:
        with connect(
                host="localhost",
                user="root",
                password="A1a1B2b2",
                database="personal_database"
        ) as connection:
            cursor = connection.cursor()
            # print sql operation
            if showOperation:
                color.printMagenta("SQL: " + sqloperation)
            cursor.execute("SET SQL_SAFE_UPDATES = 0")
            cursor.execute(sqloperation)
            result = cursor.fetchall()
            connection.commit()
            # return result of sql operation
            return result
    except Error as e:
        color.printRed(e)


def sql(showOperation, operation):
    sqloperation = input("SQL Command: ")
    if sqloperation != "":
        result = execute(sqloperation, showOperation)
        if len(result) > 0:
            columnNames = []
            for i in range(len(result[0])):
                columnNames.append("")
            functions.printTable(result, columnNames, "blue", ["cyan"], "blue", True)
        color.printGreen("Operation successfull")
        if operation.__contains__("-r") and sqloperation != "":
            sql(showOperation, operation)


def prepare(values):
    for i in range(len(values)):
        values[i] = format.value(values[i])
    return values                        
