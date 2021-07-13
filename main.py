# this is the starting point of the terminal application

# third party imports:

# first party imports:
import color
import terminalLanguage




# main function:
def main():
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
        elif operation != "":  # exits the program if operation is empty
            main()


color.printMagenta("Welcome to Jonathan's personal database")
color.printMagenta("Enter lhelp to view all possible operations")
main()
