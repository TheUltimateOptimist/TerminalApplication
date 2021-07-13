# this file contains all functions that are used to delete data from the personal database
# except the table specific delete functions

# third party imports:

# first party imports:
import sql
import color


# functions:
def deleterow(showOperation, operation):
    table = input("table: ")
    if table != "":
        whereclause = input("where clause: ")
        sql.execute(f"DELETE FROM {table} WHERE {whereclause}", showOperation)
        if operation.__contains__("-r") and table != "":
            deleterow(showOperation, operation)


def deletecolumn(showOperation, operation):
    table = input("table")
    if table != "":
        column = input("column")
        sql.execute(f"ALTER TABLE {table} DROP COLUMN {column}", showOperation)
        if operation.__contains__("-r") and table != "":
            deletecolumn(showOperation, operation)


def deletetable(showOperation, operation):
    tableName = input("table name: ")
    if tableName != "":
        if sql.execute(f"DROP TABLE {tableName}", showOperation) != None:
            color.printGreen(f"table {tableName} successfully deleted")
        if operation.__contains__("-r") and tableName != "":
            deletetable(showOperation, operation)
