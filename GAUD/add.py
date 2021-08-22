# this file contains all functions that are used to add data into the personal database
# except the table specific add functions

# third party imports:

# first party imports:
import sql
import color
from GAUD import get


# functions:
def add(showOperation, operation):
    table = input("table: ")
    if table != "":
        columnnames = get.getcolumnnames(showOperation, table)
        values = []
        j = 0
        for i in columnnames:
            if i[1].__contains__("int"):
                values.append(input(f'{i[0]}: '))
            else:
                values.append("'" + input(f'{i[0]}: ') + "'")
            j = j + 1
        s = ""
        for i in range(len(values)):
            if i < len(values) - 1:
                s = s + values[i] + ", "
            else:
                s = s + values[i]
        sql.execute(f"INSERT INTO {table} VALUES({s})", showOperation, "post")
        if operation.__contains__("-r") and table != "":
            add(showOperation, operation)


def addcolumn(showOperation, operation):
    table = input("table: ")
    if table != "":
        columndefinition = input("columnDefinition: ")
        sql.execute(
            f"ALTER TABLE {table} ADD {columndefinition}", showOperation, "post")
        if operation.__contains__("-r") and table != "":
            addcolumn(showOperation, operation)


def addtable(showOperation, operation):
    tableName = input("table name: ")
    if tableName != "":
        sqloperation = f"CREATE TABLE {tableName} ("
        numberOfColumns = int(input("number of columns: "))
        for i in range(numberOfColumns):
            columnDefinition = input(
                "name of column " + str(i + 1) + ": ") + " "
            columnDefinition = columnDefinition + input("datatype: ") + " "
            columnDefinition = columnDefinition + input("addition: ")
            if i == numberOfColumns - 1:
                columnDefinition = columnDefinition + ")"
            else:
                columnDefinition = columnDefinition + ","
            sqloperation = sqloperation + columnDefinition
        sql.execute(sqloperation, showOperation, "post")
        color.printGreen(f'table {tableName} successfully created')
        if operation.__contains__("-r") and tableName != "":
            addtable(showOperation, operation)


# intern functions
def addIntern(tableName, columns, values, showOperation):
    """
    inserts a set of values into personal database\n
    returns nothing\n
    parameters:\n
    tableName     -> table the values will be inserted into\n
    columns       -> list of the columns the values belong to the\n
                  -> ["all"]: will assume that you entered value for every column of the table\n
                  -> ["all except id"]: will assume you entered a value for every column of the table except the id column of the\n
    values        -> list of the values to be inserted into the tables\n
    showOperation -> prints sql operation if showOperation is true       
    """
    values = sql.prepare(values)
    if columns[0] == "all":
        sql.execute(
            f"INSERT INTO {tableName} VALUES({', '.join(values)})", showOperation, "post")
    elif columns[0] == "all except id":
        columnNames = get.getcolumnnames(showOperation, tableName)
        for i in range(len(columnNames)):
            columnNames[i] = columnNames[i][0]
        columnNames.pop(0)
        sql.execute(
            f"INSERT INTO {tableName}({', '.join(columnNames)}) VALUES({', '.join(values)})", showOperation, "post")
    else:
        sql.execute(
            f"INSERT INTO {tableName}({', '.join(columns)}) VALUES({', '.join(values)})", showOperation, "post")
