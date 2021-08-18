# this file contains all functions that are used to get data from the personal database
# except the table specific get functions

# third party imports:

# first party imports:
import sql
import color
import functions


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


def getColumnNames(table, showOperation):
    result = sql.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION", showOperation)
    rList = []
    for row in result:
        rList.append(str(row[0]))
    return rList    



def get(showOperation, operation):
    table = input("table: ")
    if table != "":
        all = input("all? ")
        if all == "y":
            whereclause = input("where clause: ")
            columns = getColumnNames(table, showOperation)
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
        functions.printTable(functions.toStringList(2, result), columns, "blue", ["cyan"], "blue", True)
        if operation.__contains__("-r") and table != "":
            get(showOperation, operation)



# intern functions
def getIntern(tableName, columns, whereClause, showOperation, database = "personal_database"):
    """
    retrieves data from the personal database\n
    returns a two dimensional array\n
    parameters:\n
    tableName -> name of the table to retrieve data from\n
    columns -> list of the columns that have to be retrieved\n
    whereClause -> whereClause for further specifying which values to retrieve\n
    showOperation -> if true sql operation will be printed
    """
    if whereClause != "":
        whereClause = "WHERE " + whereClause    
    if columns[0] == "all":
        columnNames = "*"
    else:
        columnNames = ", ".join(columns)
    result = sql.execute(f"SELECT {columnNames} FROM {tableName} {whereClause}", showOperation, database=database)
    finalList = []  
    for i in range(len(result)):
        list = []
        for j in range(len(result[i])):
            list.append(str(result[i][j]))
        finalList.append(list)        
    return finalList
            

        
