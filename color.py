# this file contains functions that have to do with different colors

# third party imprts:
from termcolor import colored
from colorama import init

# initialize colors
init()


# functions:
def printGreen(s):
    """
    takes a String and prints it in green
    """
    print(colored(s, "green"))


def printRed(s):
    """
    takes a String and prints it in red
    """
    print(colored(s, "red"))


def printBlue(s):
    """
    takes a String and prints it in blue
    """
    print(colored(s, "blue"))


def printMagenta(s):
    """
    takes a String and prints it in magenta
    """
    print(colored(s, "magenta"))


def printColored(s, color):
    print(colored(s, color))


def coloredText(text, color):
    return colored(text, color)
