from termcolor import colored
from colorama import init


def toStringList(dimensions, list):
    rList = []
    if dimensions == 1:
        for l in list:
            rList.append(str(l))
    elif dimensions == 2:
        for row in list:
            rowList = []
            for element in row:
                rowList.append(str(element))
            rList.append(rowList)
    return rList


def printTable(table, columnNames, columnNamesColor, entryColors, surroundingColor, showIndexes=False):
    if len(entryColors) == 1:
        for i in range(len(table) - 1):
            entryColors.append(entryColors[0])
    table = toStringList(2, table)
    if showIndexes == True:
        columnNames.reverse()
        columnNames.append("")
        columnNames.reverse()
        i = 1
        for row in table:
            row.reverse()
            row.append(str(i))
            row.reverse()
            i = i + 1
    init()
    # calculate max Lengths:
    maxLengths = []
    for i in range(len(columnNames)):
        maxLength = len(columnNames[i])
        for j in range(len(table)):
            if len(table[j][i]) > maxLength:
                maxLength = len(table[j][i])
        maxLengths.append(maxLength + 1)

    # print table
    # print top Bar
    topBar = "+"
    for l in maxLengths:
        topBar = topBar + l*"-" + "-+"
    print(colored(topBar, surroundingColor))

    # print column names
    s = colored("| ", surroundingColor)
    i = 0
    for element in columnNames:
        s = s + (f"{colored(element, columnNamesColor)}" +
                 (maxLengths[i] - len(element))*" " + colored("| ", surroundingColor))
        i = i + 1
    print(s)

    # print bottomBar
    print(colored(topBar, surroundingColor))

    # print entries
    for i in range(len(table)):
        entry = colored("| ", surroundingColor)
        for j in range(len(columnNames)):
            entry = entry + colored(table[i][j], entryColors[i]) + (
                maxLengths[j] - len(table[i][j]))*" " + colored("| ", surroundingColor)
        print(entry)

    # print end bar
    print(colored(topBar, surroundingColor))


def toOneDimList(twoDimList, choosenIndex):
    result = []
    for row in twoDimList:
        result.append(row[choosenIndex])
    return result
