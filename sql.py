# file contains functions needed for executing sql operations

# third party imports:
from mysql.connector import connect, Error

# first party imports:
import color

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
            cursor.execute("SET SQL_SAFE_UPDATES = 0")
            cursor.execute(sqloperation)
            result = cursor.fetchall()
            connection.commit()
            # print sql operation
            if showOperation:
                color.printMagenta("SQL: " + sqloperation)
            # return result of sql operation
            return result
    except Error as e:
        color.printRed(e)


def sql(showOperation, operation):
    sqloperation = input("SQL Command: ")
    if sqloperation != "":
        result = execute(sqloperation, showOperation)
        for row in result:
            color.printBlue(row)
        color.printGreen("Operation successfull")
        if operation.__contains__("-r") and sqloperation != "":
            sql(showOperation, operation)
