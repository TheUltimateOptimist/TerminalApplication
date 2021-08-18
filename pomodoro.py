# this file contains every functions that help performing the pomodoro technique

# third party imports:
import time

# first party imports:
from GAUD import get, add
from sql import execute
from format import currentDate, currentDateTime
import color


def printPomodoroCount(showOperation):
    count = str(execute(f"SELECT COUNT(start) from pomodoro WHERE day = '{currentDate()}'", showOperation)[0][0])
    color.printGreen("current count: " + count) 


def pomodoro(showOperation, sqloperation):
    for i in range(4):
        printPomodoroCount(showOperation)
        color.printGreen("Start Working!")
        start = currentDateTime()
        for j in range(27):
            time.sleep(60)
            color.printBlue(f"minutes left: {str(26 - j)}")
        add.addIntern("pomodoro", ["all"], [currentDate(), start], showOperation)  
        color.printGreen("Pomodoro finished!")
        if i != 3:
            color.printGreen("3 Minuten Pause!")
            for g in range(180):
                time.sleep(1)
                color.printBlue(str(180-1-g))   
    color.printMagenta("ONE POMODORO CYCLE FINISHED!!!!!!!!")             
