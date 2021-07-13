# this file contains all functions that help the user work with the terminal

#third party imports:

#first party imports:
import terminalLanguage
import color



#functions:
def printFunctionHelp(functionName):
    for element in terminalLanguage.allOperations:
        if element.__name__ == functionName:
            help(element)


def lhelp(irrelevantOne, irrelevantTwo):
    color.printBlue("all operations: ")
    for v in terminalLanguage.allOperations:
        color.printMagenta(v.__name__)
        color.printBlue("all additions: ")
    for s in terminalLanguage.allAdditions:
        color.printMagenta(s)


