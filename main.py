# this is the starting point of the terminal application

# third party imports:

# first party imports:
from sql import execute
import color
import terminalLanguage


# starting the server
def initializeServer():
    print("starting server...")
    result = execute("", False, "start")
    color.printGreen("server successfully started")


# interact with user
def interact():
    showOperation = False
    operation = input("What's up my friend?> ")
    if operation.__contains__("-s"):
        showOperation = True
    if operation.__contains__("-h"):
        import userHelp as h
        h.printFunctionHelp(operation)
    else:
        found = False
        for element in terminalLanguage.allOperations:
            if operation.__contains__(element.__name__):
                found = True
                element(showOperation, operation)
                break

        if not found and operation != "":
            color.printRed("ERROR: Unknown Operation")
        if operation != "":  # exits the program if operation is empty
            interact()


# main function:
if __name__ == '__main__':
    initializeServer()
    color.printMagenta("Welcome to Jonathan's personal database")
    color.printMagenta("Enter lhelp to view all possible operations")
    interact()
