# this file contains all functions that are used to update data from the personal database
# except the table specific update functions

# third party imports:

# first party imports:
import sql
import color


# functions:
def renamecolumn(showOperation, operation):
    table = input("table: ")
    if table != "":
        oldname = input("old name: ")
        newname = input("new name: ")
        sql.execute(
            f"ALTER TABLE {table} RENAME COLUMN {oldname} TO {newname}", showOperation)
        if operation.__contains__("-r") and table != "":
            renamecolumn(showOperation, operation)


def updatecompletecolumn(showOperation, operation):
    table = input("table: ")
    if table != "":
        column = input("column: ")
        isNumber = input("isNumber? ")
        # get number of rows
        count = int(str(sql.execute(f"SELECT COUNT(*) FROM {table}")[0][0], showOperation))
        for i in range(1, count + 1):
            # print current row
            color.printBlue(
                str(sql.execute(f"SELECT * FROM {table} WHERE id = {i}", showOperation)))
            new = input("newValue: ")
            if new != "":
                if isNumber == "y":
                    sql.execute(
                        f"UPDATE {table} SET {column} = {new} WHERE id = {i}", showOperation)
                else:
                    sql.execute(
                        f"UPDATE {table} SET {column} = '{new}' WHERE id = {i}", showOperation)
        if operation.__contains__("-r") and table != "":
            updatecompletecolumn(showOperation, operation)



# intern functions
def updateIntern(tableName, columns, values, whereClause ,showOperation, database = "personal_database"):
    """
    updates specific columns of a specific table using values it is given\n
    returns nothing\n
    parameters:
    tableName -> name of the table to update\n
    columns -> list of columnNames to update\n
    values -> list of values to use for updating the given columns\n
    whereClause -> the whereClause for further specifying which values to update\n
    showOperation -> if it is true the sql operation is shown
    """
    if whereClause != "":
        whereClause = "WHERE " + whereClause
    s = []
    values = sql.prepare(values)
    for i in range(len(columns)):
        s.append(columns[i] + " = " + values[i])
    sql.execute(f"UPDATE {tableName} SET {', '.join(s)} {whereClause}", showOperation, database=database)       
