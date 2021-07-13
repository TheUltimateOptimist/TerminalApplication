# this file contains all functions that are used to get data from the personal database
# except the table specific get functions

# third party imports:

# first party imports:
import sql
import color


#functions:
def getcolumnnames(showOperation, operation):
    if operation.__contains__("getcolumnnames"):
        table = input("table: ")
    else:
        table = operation
    if table != "":
        result = sql.execute(
            f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION", showOperation)
        columnNames = []
        for i in range(len(result)):
            columnNames.append(
                [str(result[i][0]), str(result[i][1]).split("'")[1]])
        if operation.__contains__("getcolumnnames"):
            for i in columnNames:
                color.printBlue(f"{i[0]} {i[1]}")
        if operation.__contains__("-r") and table != "":
            getcolumnnames(showOperation, operation)
        return columnNames


def get(showOperation, operation):
    table = input("table: ")
    if table != "":
        all = input("all? ")
        if all == "y":
            whereclause = input("where clause: ")
            columns = getcolumnnames(showOperation, table)
            if whereclause == "":
                sqloperation = f"SELECT * FROM {table}"
            else:
                sqloperation = f"SELECT * FROM {table} WHERE {whereclause}"
        else:
            columns = input("columns: ")
            whereclause = input("where clause: ")
            if whereclause == "":
                sqloperation = f"SELECT {columns} FROM {table}"
            else:
                sqloperation = f"SELECT {columns} FROM {table} WHERE {whereclause}"
            columns = columns.split(", ")
        result = sql.execute(sqloperation, showOperation)
        for r in result:
            s = ""
            for c in range(len(columns)):
                s = s + str(columns[c][0]) + ": " + str(r[c]) + " | "
            color.printBlue(s)
        if operation.__contains__("-r") and table != "":
            get(showOperation, operation)